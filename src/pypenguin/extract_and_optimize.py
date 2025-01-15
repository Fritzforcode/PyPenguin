from pypenguin.optimize import optimizeProjectJSON
from pypenguin.optimize.costumes_sounds import finalizeCostume

import urllib.parse
import os, shutil, zipfile

from pypenguin.utility import readJSONFile, writeJSONFile, insureCorrectPath, getImageSize, Platform

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
    projectFilePath         : str,
    optimizedProjectDir     : str,
    temporaryDir            : str,
    sourcePlatform          : Platform,
    deoptimizedDebugFilePath: str | None = None,
    optimizedDebugFilePath  : str | None = None,
):
    projectFilePath              = insureCorrectPath(projectFilePath         , "PyPenguin")
    optimizedProjectDir          = insureCorrectPath(optimizedProjectDir     , "PyPenguin")
    temporaryDir                 = insureCorrectPath(temporaryDir            , "PyPenguin")
    if deoptimizedDebugFilePath != None:
        deoptimizedDebugFilePath = insureCorrectPath(deoptimizedDebugFilePath, "PyPenguin")
    if optimizedDebugFilePath   != None:
        optimizedDebugFilePath   = insureCorrectPath(optimizedDebugFilePath  , "PyPenguin")
    
    # Extract the PenguinMod project
    deoptimizedData = extractProject(
        pmpFilePath=projectFilePath,
        jsonFilePath=None, # Dont write the unoptimized version to a file
        temporaryDir=temporaryDir,
    )
    if deoptimizedDebugFilePath != None:
        writeJSONFile(deoptimizedDebugFilePath, data=deoptimizedData)

    # Optimize project.json
    optimizedData = optimizeProjectJSON(
        projectData=deoptimizedData,
        sourcePlatform=sourcePlatform,
    )
    
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
            encodedSpriteName = "stage"
        else:
            encodedSpriteName = "sprite_" + urllib.parse.quote(sprite["name"])
    
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
        newCostumes = []
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
            width, height = getImageSize(file=srcPath)
            shutil.copy(
                src=srcPath,
                dst=destPath
            )
            newCostumes.append(finalizeCostume(
                data=costume,
                width=width,
                height=height,
            ))
        sprite["costumes"] = newCostumes            
        
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
    
    
    if optimizedDebugFilePath != None:
        writeJSONFile(optimizedDebugFilePath, data=optimizedData)

        
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
