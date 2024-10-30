import zipfile
import os
import shutil
from helper_functions import readJSONFile, writeJSONFile

def extract(
    pmp_file_path  : str, # Path to your .pmp file
    json_file_path : str, # Path to your final .json file,
    temporary_dir  : str, # Where the zip will be extracted
    prettyFormat   : bool = True,
):
    
    # Directory where you want to extract files
    # Path to your .zip file
    zip_file_path = "source.zip"
    
    # Copy the .pmp to file and rename it .zip
    shutil.copy(pmp_file_path, zip_file_path)
    
    # Ensure the extraction directory exists
    os.makedirs(temporary_dir, exist_ok=True)
    shutil.rmtree(temporary_dir)
    os.makedirs(temporary_dir, exist_ok=True)
    
    # Open and extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temporary_dir)
    
    # Copy project.json to your folder and rename it to [json_file_path] 
    if prettyFormat:
        json = readJSONFile(os.path.join(temporary_dir, "project.json"))
        writeJSONFile(json_file_path, json)
    else:
        shutil.copy(os.path.join(temporary_dir, "project.json"), json_file_path)
    
    
    # Delete temporary files
    os.remove(zip_file_path)


if __name__ == "__main__":
    filename = "varTest"#input("Filename: ")
    extract(
        pmp_file_path ="assets/studies/"+filename+".pmp",
        json_file_path="assets/studies/"+filename+".json",
    )
