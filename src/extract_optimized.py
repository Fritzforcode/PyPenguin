from validate import validateProject
from source_extractor import extractProject
from optimize import optimizeProjectJSON
from deoptimize import deoptimizeProject

import urllib.parse
import os, shutil

from helper_functions import readJSONFile, writeJSONFile, pp

projectFilePath    = "assets/studies/example.pmp"
optimizedPath      = "assets/optimized.json"
assetDirectory     = "projectAssets/"
temporaryDirectory = "temporary/"

unoptimizedData = extractProject(
    pmpFilePath=projectFilePath,
    jsonFilePath=None, # Dont write the unoptimized version to a file
    temporaryDir=temporaryDirectory,
)
optimizedData = optimizeProjectJSON(
    projectData=unoptimizedData
)
writeJSONFile(filePath=optimizedPath, data=optimizedData)

validateProject(
    projectData=optimizedData
)

# Clear the directory
os.makedirs(assetDirectory, exist_ok=True)
shutil.rmtree(path=assetDirectory)


for sprite in optimizedData["sprites"]:
    if sprite["isStage"]:
        encodedSpriteName = "#Stage"
    else:
        encodedSpriteName = urllib.parse.quote(sprite["name"])

    os.makedirs(assetDirectory+encodedSpriteName+"/costumes", exist_ok=True)
    for costume in sprite["costumes"]:
        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
        shutil.copy(
            src=temporaryDirectory + oldCostumeName,
            dst=assetDirectory + encodedSpriteName + "/costumes/" + encodedCostumeName,
        )
    
    os.makedirs(assetDirectory+encodedSpriteName+"/sounds", exist_ok=True)
    for costume in sprite["sounds"]:
        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
        shutil.copy(
            src=temporaryDirectory + oldCostumeName,
            dst=assetDirectory + encodedSpriteName + "/sounds/" + encodedCostumeName,
        )

# Remove the temporary directory
shutil.rmtree(temporaryDirectory)


deoptimizeProject(
    sourcePath=optimizedPath,
    targetPath="assets/deoptimized.json"
)