from validate import validateProject
from source_extractor import extractProject
from optimize import optimizeProject
from deoptimize import deoptimizeProject

import urllib.parse
import os, shutil

from helper_functions import readJSONFile, writeJSONFile, pp

projectFilePath    = "assets/studies/example.pmp"
optimizedPath      = "assets/optimized.json"
directory          = "projectAssets/"
temporaryDirectory = "temporary/"

unoptimizedData = extractProject(
    pmpFilePath=projectFilePath,
    jsonFilePath=None, # Dont write the unoptimized version to a file
    temporaryDir=temporaryDirectory,
)
optimizedData = optimizeProject(
    projectData=unoptimizedData
)
writeJSONFile(filePath=optimizedPath, data=optimizedData)

validateProject(
    projectData=optimizedData
)

# Clear the directory
os.makedirs(directory, exist_ok=True)
shutil.rmtree(path=directory)


for sprite in optimizedData["sprites"]:
    if sprite["isStage"]:
        encodedSpriteName = "#Stage"
    else:
        encodedSpriteName = urllib.parse.quote(sprite["name"])

    os.makedirs(directory+encodedSpriteName+"/costumes", exist_ok=True)
    for costume in sprite["costumes"]:
        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
        shutil.copy(
            src=temporaryDirectory + oldCostumeName,
            dst=directory + encodedSpriteName + "/costumes/" + encodedCostumeName,
        )
    
    os.makedirs(directory+encodedSpriteName+"/sounds", exist_ok=True)
    for costume in sprite["sounds"]:
        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
        shutil.copy(
            src=temporaryDirectory + oldCostumeName,
            dst=directory + encodedSpriteName + "/sounds/" + encodedCostumeName,
        )

# Remove the temporary directory
shutil.rmtree(temporaryDirectory)


deoptimizeProject(
    sourcePath=optimizedPath,
    targetPath="assets/deoptimized.json"
)