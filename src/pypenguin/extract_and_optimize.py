from pypenguin.validate import validateProject, ValidationError
from pypenguin.optimize import optimizeProjectJSON

import urllib.parse
import os, shutil, zipfile

from pypenguin.helper_functions import readJSONFile, writeJSONFile, insureCorrectPath

def extractProject(
    pmpFilePath       : str, # Path to your .pmp file
    jsonFilePath      : None|str, # Path to your final .json file,
    temporaryDir      : str, # Where the zip will be extracted
    prettyFormat      : bool = True,
    deleteTemporaryDir: bool = False,
):
    pmpFilePath  = insureCorrectPath(pmpFilePath , "PyPenguin")
    jsonFilePath = insureCorrectPath(jsonFilePath, "PyPenguin")
    temporaryDir = insureCorrectPath(temporaryDir, "PyPenguin")
    zipFilePath  = insureCorrectPath("source.zip", "PyPenguin")
    
    # Copy the .pmp to file and rename it .zip
    shutil.copy(pmpFilePath, zipFilePath)
    
    # Ensure the extraction Dir exists
    os.makedirs(temporaryDir, exist_ok=True)
    shutil.rmtree(temporaryDir)
    os.makedirs(temporaryDir, exist_ok=True)
    
    # Open and extract the zip file
    with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
        zip_ref.extractall(temporaryDir)
    
    
    json = readJSONFile(os.path.join(temporaryDir, "project.json"))
    if jsonFilePath != None:
        # Copy project.json to your folder and rename it to [json_file_path] 
        if prettyFormat:
            writeJSONFile(jsonFilePath, json)
        else:
            shutil.copy(os.path.join(temporaryDir, "project.json"), jsonFilePath)
    
    
    # Delete temporary files
    os.remove(zipFilePath)
    if deleteTemporaryDir:
        shutil.rmtree(temporaryDir)
    return json

def extractAndOptimizeProject(
    projectFilePath    : str,
    optimizedProjectDir: str,
    temporaryDir       : str,
    writeDebugFiles    : bool = False,
):
    projectFilePath     = insureCorrectPath(projectFilePath , "PyPenguin")
    optimizedProjectDir = insureCorrectPath(optimizedProjectDir, "PyPenguin")
    temporaryDir        = insureCorrectPath(temporaryDir, "PyPenguin")
    temp1FilePath       = insureCorrectPath("temp.json",  "PyPenguin")
    temp2FilePath       = insureCorrectPath("temp2.json", "PyPenguin")
    
    # Extract the PenguinMod project
    deoptimizedData = extractProject(
        pmpFilePath=projectFilePath,
        jsonFilePath=None, # Dont write the unoptimized version to a file
        temporaryDir=temporaryDir,
    )
    if writeDebugFiles: writeJSONFile(temp1FilePath, data=deoptimizedData)

    # Optimize project.json
    optimizedData = optimizeProjectJSON(
        projectData=deoptimizedData,
    )
    if writeDebugFiles: writeJSONFile(temp2FilePath, data=optimizedData)
    
    # Make sure the project Dir exists
    os.makedirs(optimizedProjectDir, exist_ok=True)
    
    # Clear the project Dir
    os.makedirs(optimizedProjectDir, exist_ok=True)
    shutil.rmtree(path=optimizedProjectDir)
    
    # Reorganize Assets
    for i, sprite in enumerate(optimizedData["sprites"]):
        deoptimizedSprite  = deoptimizedData["targets"][i]
        # Encode the sprite name
        if sprite["isStage"]:
            encodedSpriteName = "#Stage"
        else:
            encodedSpriteName = urllib.parse.quote(sprite["name"])
    
        # Make sure the sprite dir has the costume dir
        os.makedirs(
            os.path.join(
                optimizedProjectDir,
                encodedSpriteName,
                "costumes",
            ), 
            exist_ok=True
        )
        # Copy and rename costumes
        for j, costume in enumerate(sprite["costumes"]):
            deoptimizedCostume = deoptimizedSprite["costumes"][j]
            oldCostumeName     =      deoptimizedCostume["assetId"] + "." + costume["extension"]
            encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["extension"])
            srcPath = os.path.join(temporaryDir, oldCostumeName)
            destPath = os.path.join(
                optimizedProjectDir, 
                encodedSpriteName, 
                "costumes", 
                encodedCostumeName
            )
            shutil.copy(
                src=srcPath,
                dst=destPath
            )

        
        # Make sure the sprite dir has the sounds dir
        os.makedirs(
            os.path.join(
                optimizedProjectDir,
                encodedSpriteName,
                "sounds",
            ), 
            exist_ok=True
        )
        # Copy and rename sounds            
        for j, sound in enumerate(sprite["sounds"]):
            deoptimizedSound = deoptimizedSprite["sounds"][j]
            oldSoundName     =      deoptimizedSound["assetId"] + "." + sound["extension"]
            encodedSoundName = urllib.parse.quote(sound["name"] + "." + sound["extension"])
            srcPath = os.path.join(temporaryDir, oldSoundName)
            destPath = os.path.join(
                optimizedProjectDir, 
                encodedSpriteName, 
                "sounds", 
                encodedSoundName
            )
            shutil.copy(
                src=srcPath,
                dst=destPath
            )
    
    # Add the optimized project.json
    writeJSONFile(
        filePath=os.path.join(optimizedProjectDir, "project.json"), 
        data=optimizedData,
    )
    
    # Remove the temporary Dir
    shutil.rmtree(temporaryDir)
    return optimizedData

if __name__ == "__main__":
    extractAndOptimizeProject(
        projectFilePath           = "assets/studies/jsonBlocks.pmp",
        optimizedProjectDir = "optimizedProject/",
        temporaryDir        = "temporary/",
    )
