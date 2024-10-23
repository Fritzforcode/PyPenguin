import zipfile
import os
import shutil
from helper_functions import readJSONFile, writeJSONFile

def extract(
    pmp_file_path  : str  = "source.pmp",  # Path to your .pmp file
    json_file_path : str  = "source.json", # Path to your final .json file
    prettyFormat   : bool = True,
):
    
    # Directory where you want to extract files
    extract_dir = 'temporary/'
    # Path to your .zip file
    zip_file_path = "source.zip"
    
    # Copy the .pmp to file and rename it .zip
    shutil.copy(pmp_file_path, zip_file_path)
    
    # Ensure the extraction directory exists
    os.makedirs(extract_dir, exist_ok=True)
    
    # Open and extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Copy project.json to your folder and rename it to [json_file_path] 
    if prettyFormat:
        json = readJSONFile(os.path.join(extract_dir, "project.json"))
        writeJSONFile(json_file_path, json)
    else:
        shutil.copy(os.path.join(extract_dir, "project.json"), json_file_path)
    
    
    # Delete temporary files
    os.remove(zip_file_path)
    #shutil.rmtree(extract_dir)


if __name__ == "__main__":
    filename = input("Filename: ")
    extract(
        pmp_file_path ="assets/studies/"+filename+".pmp",
        json_file_path="assets/studies/"+filename+".json",
    )
