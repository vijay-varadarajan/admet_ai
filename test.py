from admet_ai.admet_predict import admet_predict

# Load the model
result = admet_predict(data_path='../Virtual-drug-screening-pipeline/output/smiles_raw.csv', smiles_column='Smiles', save_path='temp_results.csv')
