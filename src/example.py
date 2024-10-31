from validate import validateProject
from source_extractor import extract
from optimize import optimize

import urllib.parse
import os, shutil

from helper_functions import readJSONFile, pp

directory          = "projectAssets/"
temporaryDirectory = "temporary/"
jsonPath           = "assets/studies/test.json"
optimizedPath      = "assets/optimized.json"
#extract(
#    pmp_file_path="../assets/studies/assetTest.pmp",
#    json_file_path=jsonPath,
#    temporary_dir=temporaryDirectory,
#)
#optimize(
#    sourcePath=jsonPath,
#    targetPath=optimizedPath,
#)

#os.makedirs(directory, exist_ok=True)
#shutil.rmtree(path=directory)

data = readJSONFile(optimizedPath)
pp(data)
validateProject(data=data)

#for sprite in data["sprites"]:
#    if sprite["isStage"]:
#        encodedSpriteName = "#Stage"
#    else:
#        encodedSpriteName = urllib.parse.quote(sprite["name"])
#
#    os.makedirs(directory+encodedSpriteName+"/costumes", exist_ok=True)
#    for costume in sprite["costumes"]:
#        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
#        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
#        shutil.copy(
#            src=temporaryDirectory + oldCostumeName,
#            dst=directory + encodedSpriteName + "/costumes/" + encodedCostumeName,
#        )
#    
#    os.makedirs(directory+encodedSpriteName+"/sounds", exist_ok=True)
#    for costume in sprite["sounds"]:
#        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
#        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
#        shutil.copy(
#            src=temporaryDirectory + oldCostumeName,
#            dst=directory + encodedSpriteName + "/sounds/" + encodedCostumeName,
#        )
#shutil.rmtree(temporaryDirectory)
# test name overlapping