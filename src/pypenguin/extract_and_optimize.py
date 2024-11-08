from .validate import validateProject, ValidationError
from .optimize import optimizeProjectJSON

import urllib.parse
import os, shutil, zipfile

from .helper_functions import readJSONFile, writeJSONFile, pp

def extractProject(
    pmpFilePath       : str, # Path to your .pmp file
    jsonFilePath      : None|str, # Path to your final .json file,
    temporaryDir      : str, # Where the zip will be extracted
    prettyFormat      : bool = True,
    deleteTemporaryDir: bool = False,
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

def extractAndOptimizeProject(
    projectFilePath: str,
    optimizedProjectDirectory: str,
    temporaryDirectory: str,
    writeDebugFiles   : bool = False,
):
    # Extract the PenguinMod project
    deoptimizedData = extractProject(
        pmpFilePath=projectFilePath,
        jsonFilePath=None, # Dont write the unoptimized version to a file
        temporaryDir=temporaryDirectory,
    )
    if writeDebugFiles: writeJSONFile("temp.json", data=deoptimizedData)

    # Optimize project.json
    optimizedData = optimizeProjectJSON(
        projectData=deoptimizedData,
    )
    if writeDebugFiles: writeJSONFile("temp2.json", data=optimizedData)
    
    # Make sure the project directory exists
    os.makedirs(optimizedProjectDirectory, exist_ok=True)
    
    # Validate the optimized project.json and halde errors
    try:
        validateProject(
            projectData=optimizedData,
        )
    except ValidationError as error:
        print(error)
        print("This error is likely the fault of the developer. Please report this.")
    
    # Clear the project directory
    os.makedirs(optimizedProjectDirectory, exist_ok=True)
    shutil.rmtree(path=optimizedProjectDirectory)
    
    # Reorganize Assets
    for sprite in optimizedData["sprites"]:
        # Encode the sprite name
        if sprite["isStage"]:
            encodedSpriteName = "#Stage"
        else:
            encodedSpriteName = urllib.parse.quote(sprite["name"])
    
        # Make sure the sprite dir has the costume dir
        os.makedirs(
            os.path.join(
                optimizedProjectDirectory,
                encodedSpriteName,
                "costumes",
            ), 
            exist_ok=True
        )
        # Copy and rename costumes
        for costume in sprite["costumes"]:
            oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            shutil.copy(
                src=os.path.join(temporaryDirectory, oldCostumeName),
                dst=os.path.join(
                    optimizedProjectDirectory, 
                    encodedSpriteName, 
                    "costumes", 
                    encodedCostumeName
                ),
            )
        
        # Make sure the sprite dir has the sounds dir
        os.makedirs(
            os.path.join(
                optimizedProjectDirectory,
                encodedSpriteName,
                "sounds",
            ), 
            exist_ok=True
        )
        # Copy and rename sounds
        for costume in sprite["sounds"]:
            oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
            shutil.copy(
                src=os.path.join(temporaryDirectory, oldCostumeName),
                dst=os.path.join(
                    optimizedProjectDirectory, 
                    encodedSpriteName, 
                    "sounds", 
                    encodedCostumeName
                ),
            )
    
    # Add the optimized project.json
    writeJSONFile(
        filePath=os.path.join(optimizedProjectDirectory, "project.json"), 
        data=optimizedData,
    )
    
    # Remove the temporary directory
    shutil.rmtree(temporaryDirectory)
    return optimizedData

if __name__ == "__main__":
    extractAndOptimizeProject(
        projectFilePath           = "assets/studies/jsonBlocks.pmp",
        optimizedProjectDirectory = "optimizedProject/",
        temporaryDirectory        = "temporary/",
    )
