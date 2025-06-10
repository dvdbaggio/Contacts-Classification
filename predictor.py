import os
import argparse
from Bio.PDB import PDBList 

def parse_args():
    parser = argparse.ArgumentParser(description="Predict contact types of a given protein structure.")
    parser.add_argument('--input', type=str, required=True, help='PDB ID of the protein structure to predict.')
    parser.add_argument('--model', type=str, required=True, help='Name of the trained model file.')
    return parser.parse_args()

def retrieve_structure(pdb_id):
    pdb_file = PDBList.retrieve_pdb_file(pdb_id, file_format='pdb', pdir='./data/pdb files/', overwrite=True)
    if not pdb_file:
        raise ValueError(f"Failed to retrieve PDB file for ID: {pdb_id}")
    os.system(f"python3 ./data/script/calc_features.py ./data/pdb files/{pdb_id}.cif -out_dir ./data/output features/")
    

def main():
    args = parse_args()
    pdb_id = args.input
    model_name = args.model

