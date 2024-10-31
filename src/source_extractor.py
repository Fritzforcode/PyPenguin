import zipfile
import os
import shutil
from helper_functions import readJSONFile, writeJSONFile

def extractProject(
    pmpFilePath       : str, # Path to your .pmp file
    jsonFilePath      : None|str, # Path to your final .json file,
    temporaryDir      : str, # Where the zip will be extracted
    prettyFormat      : bool = True,
    deleteTemporaryDir: bool = False
):
    # Directory where you want to extract files
    # Path to your .zip file
    zip_file_path = "source.zip"
    
    # Copy the .pmp to file and rename it .zip
    shutil.copy(pmpFilePath, zip_file_path)
    
    # Ensure the extraction directory exists
    os.makedirs(temporaryDir, exist_ok=True)
    shutil.rmtree(temporaryDir)
    os.makedirs(temporaryDir, exist_ok=True)
    
    # Open and extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temporaryDir)
    
    
    json = readJSONFile(os.path.join(temporaryDir, "project.json"))
    if jsonFilePath != None:
        # Copy project.json to your folder and rename it to [json_file_path] 
        if prettyFormat:
            writeJSONFile(jsonFilePath, json)
        else:
            shutil.copy(os.path.join(temporaryDir, "project.json"), jsonFilePath)
    
    
    # Delete temporary files
    os.remove(zip_file_path)
    if deleteTemporaryDir:
        shutil.rmtree(temporaryDir)
    return json

