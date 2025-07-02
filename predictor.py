import argparse, os
import logging
import pandas as pd
from Bio.PDB import PDBList
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import xgboost as xgb

def parse_args():
    """Parse command line arguments.""" 
    parser = argparse.ArgumentParser(description="Predict contact types of a given protein structure.")
    parser.add_argument('--input', type=str, required=True, help='PDB ID of the protein structure to predict.')
    parser.add_argument('--model', type=str, required=True, help='Type of model to use for prediction (e.g., "mcc", "ova").')
    return parser.parse_args()

def retrieve_features(pdb_id):
    """Retrieve PDB features and 3DI data for a given PDB ID."""
    logging.info(f"Retrieving features for PDB ID: {pdb_id}...")
    os.makedirs('./data/output_features', exist_ok=True)
    os.makedirs('./data/output_3di', exist_ok=True)

    pdblist = PDBList()
    pdb_file = pdblist.retrieve_pdb_file(pdb_id, pdir='./data/pdb_files/', overwrite=True)
    if not pdb_file:
        logging.error(f"Failed to retrieve PDB file for ID: {pdb_id}")
        raise ValueError(f"Failed to retrieve PDB file for ID: {pdb_id}")
    # Retrieve PDB features
    os.system(f"python3 ./data/script/calc_features.py ./data/pdb_files/{pdb_id}.cif -out_dir ./data/output_features/")
    # Retrieve 3DI features
    os.system(f"python3 ./data/script/calc_3di.py ./data/pdb_files/{pdb_id}.cif -out_dir ./data/output_3di/")

    logging.info(f"Features for {pdb_id} retrieved successfully.")

    logging.info("Merging features and 3di data...")

    # Paths for the features and 3di files
    features_file = f'data/output_features/{pdb_id}.tsv'
    threed_file = f'data/output_3di/{pdb_id}.tsv'

    # Read the files
    features_df = pd.read_csv(features_file, sep='\t')
    threed_df = pd.read_csv(threed_file, sep='\t')

    # Keep only the necessary columns from the 3di file
    threed_df_subset = threed_df[['ch','resi', 'ins', 'resn', '3di_state']]

    # Merge for source residues
    merged_df = pd.merge(
        features_df,
        threed_df_subset,
        how='left',
        left_on=['s_ch', 's_resi', 's_ins', 's_resn'],
        right_on=['ch','resi', 'ins', 'resn']
    )

    # Rename the merged column
    merged_df = merged_df.rename(columns={'3di_state': 's_3di_state'})

    # Drop the unnecessary columns from the first merge
    merged_df = merged_df.drop(columns=['ch','resi', 'ins', 'resn'])

    # Merge for target residues
    merged_df = pd.merge(
        merged_df,
        threed_df_subset,
        how='left',
        left_on=['t_ch', 't_resi', 't_ins', 't_resn'],
        right_on=['ch','resi', 'ins', 'resn']
    )

    # Rename the merged column
    merged_df = merged_df.rename(columns={'3di_state': 't_3di_state'})

    # Drop the unnecessary columns from the second merge
    merged_df = merged_df.drop(columns=['ch','resi', 'ins', 'resn'])

    logging.info("Features and 3di data merged successfully.")

    return merged_df

def preprocess_features(df):
    """Preprocess the features DataFrame."""

    logging.info("Preprocessing features...")

    le = LabelEncoder()
    # Mask the columns that are needed for the model
    X = df[['s_ss8','s_rsa', 's_phi', 's_psi', 's_a1', 's_a2', 's_a3', 's_a4', 's_a5', 's_3di_state', 
        't_ss8', 't_rsa', 't_phi', 't_psi', 't_a1', 't_a2', 't_a3', 't_a4', 't_a5', 't_3di_state']].copy()
    
    # Encode ss8 feature
    X['s_ss8_encoded'] = le.fit_transform(X['s_ss8'])
    X['t_ss8_encoded'] = le.fit_transform(X['t_ss8'])
    X = X.drop(columns=['s_ss8', 't_ss8'])
    
    # Fill None value with mean of the column
    X = X.apply(lambda x: x.fillna(x.mean()) if x.dtype.kind in 'biufc' else x)

    logging.info("Features preprocessed successfully.")

    return X

def predict_contacts(pdb_id, model_type = 'mcc'):
    """Predict contact types for a given PDB ID using the specified model type."""

    # Retrieve features and 3DI data
    features = retrieve_features(pdb_id)
    if features.empty:
        logging.error(f"No features retrieved for PDB ID: {pdb_id}")
        raise ValueError(f"No features retrieved for PDB ID: {pdb_id}")
    
    # Preprocess the features
    preprocessed_features = preprocess_features(features)
    if preprocessed_features.empty:
        logging.error(f"Preprocessed features are empty for PDB ID: {pdb_id}")
        raise ValueError(f"Preprocessed features are empty for PDB ID: {pdb_id}")

    # Map interaction labels to numerical values
    labels = {
        "HBOND": 0,
        "VDW": 1,
        "PIPISTACK": 2,
        "IONIC": 3,
        "PICATION": 4,
        "SSBOND": 5,
        "PIHBOND": 6,
        "Unclassified": 7
    }

    # Selected multiclassifier model
    if model_type == 'mcc':
        logging.info("Using multiclassifier model for prediction...")

        # Load the multiclass model
        model_path = 'data/models/xgboost_smote_model_mcc.json'
        if not os.path.exists(model_path):
            logging.warning(f"Model file not found: {model_path}")
            raise FileNotFoundError(f"Model directory does not exist: {model_path}")
        
        model = xgb.Booster()
        model.load_model(model_path)

        xgbMatrix = xgb.DMatrix(preprocessed_features)
        # Make predictions
        output = np.argmax(model.predict(xgbMatrix), axis=1)
        preprocessed_features['Interaction'] = output
        # Mapping numerical labels to string labels
        preprocessed_features['Interaction'] = preprocessed_features['Interaction'].map(lambda x: list(labels.keys())[x])
        # Save the predictions
        os.makedirs('./data/output_prediction', exist_ok=True)
        preprocessed_features.to_csv(f'./data/output_prediction/{pdb_id}_predicted.tsv', sep='\t', index=False)
       
    else:   # model == 'ova'
        logging.info("Using OVA model for prediction...")

        # Load multiple binary models for OVA
        models_dir = 'data/models/bin_models'
        if not os.path.exists(models_dir):
            logging.warning(f"Model directory not found: {models_dir}")
            raise FileNotFoundError(f"Model directory does not exist: {models_dir}")

        model_files = [f for f in os.listdir(models_dir) if f.endswith('.json')]
        if not model_files:
            logging.warning("No model files found in the specified directory.")
            raise FileNotFoundError("No model files found in the specified directory.")
        
        models = []
        for class_num in range(8):  
            model_path = os.path.join(models_dir, f"xgboost_model_class_{class_num}.json")
            if os.path.exists(model_path):
                model = xgb.Booster()
                model.load_model(model_path)
                models.append(model)
            else:
                logging.warning(f"Model file not found: {model_path}")

        if not models:
            logging.warning("No valid OVA models loaded.")
            raise ValueError("No valid OVA models loaded.")

        xgbMatrix = xgb.DMatrix(preprocessed_features)
        # Collect class prediction probabilities 
        probas = []

        for model in models:
            # Get class probability from each model
            proba = model.predict(xgbMatrix)
            probas.append(proba)

        probas = np.column_stack(probas)

        # Select the class with the highest probability
        preprocessed_features['Interaction'] = np.argmax(probas, axis=1)
        preprocessed_features['Interaction'] = preprocessed_features['Interaction'].map(lambda x: list(labels.keys())[x])

        preprocessed_features.to_csv(f'./data/output_prediction/{pdb_id}_predicted.tsv', sep='\t', index=False)

    logging.info(f"Predictions for {pdb_id} completed successfully.")
    logging.info(f'Predicted contacts of {pdb_id} saved to ./data/output_prediction/{pdb_id}_predicted.tsv')

def main():
    args = parse_args()

    # Set the logger
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    # Set the arguments
    pdb_id = args.input
    model_type = args.model

    if not pdb_id:
        logging.warning("No PDB ID provided for prediction.")
        raise ValueError("PDB ID is required for prediction.")

    if model_type not in ['mcc', 'ova']:
        logging.warning("Invalid model type provided. Must be either 'mcc' or 'ova'.")
        raise ValueError("Model type must be either 'mcc' or 'ova'.")

    try:
        predict_contacts(pdb_id, model_type)
    except Exception as e:
        logging.warning(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Example usage: python predictor.py --input 1aba --model multiclass

