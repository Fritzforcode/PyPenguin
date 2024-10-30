from validate import validate
from source_extractor import extract
from optimize import optimize

import urllib.parse
import os, shutil

from helper_functions import readJSONFile, pp

directory = "projectAssets/"
temporaryDirectory = "temporary/"
jsonPath = "assets/studies/test.json"
optimizedPath = "assets/test.json"
extract(
    pmp_file_path="assets/studies/assetTest.pmp",
    json_file_path=jsonPath,
    temporary_dir=temporaryDirectory,
)
optimize(
    sourcePath=jsonPath,
    targetPath=optimizedPath,
)

os.makedirs(directory, exist_ok=True)
shutil.rmtree(path=directory)

data = readJSONFile(optimizedPath)
validate(data=data)
for sprite in data["sprites"]:
    encoded_sprite_name = urllib.parse.quote(sprite["name"])

    os.makedirs(directory+encoded_sprite_name+"/costumes", exist_ok=True)
    for costume in sprite["costumes"]:
        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
        shutil.copy(
            src="temporary/" + oldCostumeName,
            dst=directory + encoded_sprite_name + "/costumes/" + encodedCostumeName,
        )
    
    os.makedirs(directory+encoded_sprite_name+"/sounds", exist_ok=True)
    for costume in sprite["sounds"]:
        oldCostumeName                    = costume["fileStem"] + "." + costume["dataFormat"]
        encodedCostumeName = urllib.parse.quote(costume["name"] + "." + costume["dataFormat"])
        shutil.copy(
            src="temporary/" + oldCostumeName,
            dst=directory + encoded_sprite_name + "/sounds/" + encodedCostumeName,
        )
shutil.rmtree(temporaryDirectory)
