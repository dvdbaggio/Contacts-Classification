# Contacts classification
This repository contains the project for classifying contacts using Machine Learning and Bioinformatics tools with the goal to accurately identify and categorize contacts within protein structures, which is crucial for understanding protein functions and interactions.

## Table of Contents
    
-   [Requirements](#requirements)

-   [Repository Structure](#repository-structure)

-   [Usage](#usage)

-   [Authors](#authors)


## Requirements

Before running the code, ensure you have Python 3.x installed. The project uses the following Python packages (installable via `pip`):
-   `pandas`
-   `Bio`
-   `scikit-learn`  
-   `numpy`
-   `xgboost`
-   `seaborn`
-   `matplotlib`
-   `imbalanced-learn`

You can install these, for example, by running:

```bash
pip install pandas Bio scikit-learn numpy xgboost
```

## Repository Structure
The repository is organized as follows:
-   **`data`**: Contains the scripts and the folders for saving the generated models and results.
    * `models`: Must contain the models trained
    * `output_3di`: Contains the *3di* features extractred by `calc_3di.py`
    * `output_features`: Contains the features extracted by `calc_features.py`
    * `output_prediction`: Contains the file with the predicted labels
-   **`contacts_prediction_mcc.ipynb`**: Jupyter notebook demonstrating model training and evaluation for the Multi-Class Classifier.
-   **`contacts_prediction_ova.ipynb`**: Jupyter notebook for training and evaluating a One-vs-All classifier.
-   **`predictor.py`**: Python CLI script for running contact classification predictions on new data.


## Usage
1.  **Clone the repository:**
    ```bash    
    git clone https://github.com/dvdbaggio/Contacts-Classification.git
    cd Contacts-Classification
    ```
    
2.  **Install dependencies:**  
    Ensure the required Python packages are installed (see _Requirements_).

3.  **Download the dataset and models:**  
    - Download the [dataset](https://drive.google.com/file/d/1Nwg_mJOL7yQjX_y9efluS1zQH8eiW_wJ/view?usp=sharing), then place it into the root of the project   

    - Download the pre-trained models from the following links or use the training Jupyter notebooks to train your own models.
        -   [Multi-Class Classifier Model](https://drive.google.com/file/d/1f_qCApT9tkHxwpiEl--i4rc8fb8Ch3tq/view?usp=sharing)
        -   [One-vs-All Classifier Model](https://drive.google.com/file/d/1mH8aaAKgGL9ewj_YG4dpCbBFiS_eFwY1/view?usp=share_link)

    If downloaded the trained models, place them into `./data/models/` folder.
    
4.  **Run the prediction script:**  
    Invoke the `predictor.py` script and provide the necessary arguments to classify contacts in your protein data:
    - `input`: PDB-ID of the protein structure.
    - `model`: Type of model to use ('mcc' or 'ova').

    ```bash
    python predictor.py --input <PDB-ID> --model <model_type>
    ```

Results will be saved in the `./data/output_prediction/` directory, with predictions for each residue pair in the specified PDB structure.

## Authors

This project was developed by:

-   Davide Baggio - 2119982
-   Sebastiano Sanson - 2130917


