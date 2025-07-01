import argparse, os
import logging
import pandas as pd
from Bio.PDB import PDBList
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import xgboost as xgb

def parse_args():
    parser = argparse.ArgumentParser(description="Predict contact types of a given protein structure.")
    parser.add_argument('--input', type=str, required=True, help='PDB ID of the protein structure to predict.')
    parser.add_argument('--model', type=str, required=True, help='Type of model to use for prediction (e.g., "multiclass", "ova").')
    # parser.add_argument('--path', type=str, required=True, help='Path to the file containing the model files.')
    return parser.parse_args()

def retrieve_features(pdb_id):
    os.makedirs('./data/output_features', exist_ok=True)
    os.makedirs('./data/output_3di', exist_ok=True)

    pdblist = PDBList()
    pdb_file = pdblist.retrieve_pdb_file(pdb_id, pdir='./data/pdb_files/', overwrite=True)
    if not pdb_file:
        logging.error(f"Failed to retrieve PDB file for ID: {pdb_id}")
        raise ValueError(f"Failed to retrieve PDB file for ID: {pdb_id}")
    # Extract features using the scripts:
    # Retrieve PDB features
    os.system(f"python3 ./data/script/calc_features.py ./data/pdb_files/{pdb_id}.cif -out_dir ./data/output_features/")
    # Retrieve 3DI features
    os.system(f"python3 ./data/script/calc_3di.py ./data/pdb_files/{pdb_id}.cif -out_dir ./data/output_3di/")

    logging.info(f"Features for {pdb_id} retrieved successfully.")

    logging.info("Merging features and 3di data...")

    # Correct the file paths
    features_file = f'data/output_features/{pdb_id}.tsv'
    threed_file = f'data/output_3di/{pdb_id}.tsv'

    # Read the files, skipping the comment line
    features_df = pd.read_csv(features_file, sep='\t')
    threed_df = pd.read_csv(threed_file, sep='\t')

    logging.info("Features and 3di files read successfully.")

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
    le = LabelEncoder()
    # Explicitly create a copy of the DataFrame slice
    X = df[['s_ss8','s_rsa', 's_phi', 's_psi', 's_a1', 's_a2', 's_a3', 's_a4', 's_a5', 's_3di_state', 
        't_ss8', 't_rsa', 't_phi', 't_psi', 't_a1', 't_a2', 't_a3', 't_a4', 't_a5', 't_3di_state']].copy()
    
    X['s_ss8_encoded'] = le.fit_transform(X['s_ss8'])
    X['t_ss8_encoded'] = le.fit_transform(X['t_ss8'])
    X = X.drop(columns=['s_ss8', 't_ss8'])
    
    # Fill None value with mean of the column
    X = X.apply(lambda x: x.fillna(x.mean()) if x.dtype.kind in 'biufc' else x)

    logging.info("Features preprocessed successfully.")

    return X

def predict_contacts(pdb_id, model_type = 'multiclass'):
    features = retrieve_features(pdb_id)
    # Preprocess features
    preprocessed_features = preprocess_features(features)

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

    if model_type == 'multiclass':
        logging.info("Using multiclass model for prediction...")

        model_path = 'data/models/xgboost_model_mcc.json'
        if not os.path.exists(model_path):
            logging.warning(f"Model file not found: {model_path}")
            raise FileNotFoundError(f"Model directory does not exist: {model_path}")
        
        model = xgb.Booster()
        model.load_model(model_path)

        xgbMatrix = xgb.DMatrix(preprocessed_features)
        output = np.argmax(model.predict(xgbMatrix), axis=1)
        preprocessed_features['Interaction'] = output
        # Convert numerical labels back to string labels
        preprocessed_features['Interaction'] = preprocessed_features['Interaction'].map(lambda x: list(labels.keys())[x])

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
        

        logging.info(f"Loading {len(model_files)} OVA models from {models_dir}...")
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
        
        logging.info(f"Loaded {len(models)} OVA models successfully.")

        # Prepare the DMatrix for prediction
        xgbMatrix = xgb.DMatrix(preprocessed_features)

        probas = []

        for model in models:
            # Get class probability from each model
            proba = model.predict(xgbMatrix)
            probas.append(proba)

        probas = np.column_stack(probas)

        # Convert probabilities to class labels
        preprocessed_features['Interaction'] = np.argmax(probas, axis=1)
        preprocessed_features['Interaction'] = preprocessed_features['Interaction'].map(lambda x: list(labels.keys())[x])

        preprocessed_features.to_csv(f'./data/output_prediction/{pdb_id}_predicted.tsv', sep='\t', index=False)

    logging.info(f"Predictions for {pdb_id} completed successfully.")

def main():
    args = parse_args()

    # Set the logger
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    pdb_id = args.input
    model_type = args.model

    if not pdb_id:
        logging.warning("No PDB ID provided for prediction.")
        raise ValueError("PDB ID is required for prediction.")

    if model_type not in ['multiclass', 'ova']:
        logging.warning("Invalid model type provided. Must be either 'multiclass' or 'ova'.")
        raise ValueError("Model type must be either 'multiclass' or 'ova'.")

    try:
        predict_contacts(pdb_id, model_type)
        logging.info(f'Predicted contacts of {pdb_id} saved to ./data/output_prediction/{pdb_id}_predicted.tsv')
    except Exception as e:
        logging.warning(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Example usage: python predictor.py --input 1aba --model multiclass

