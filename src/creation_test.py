with open("/storage/emulated/0/Download/video_uri.txt", "r") as file:
    uri = file.read()


scriptA = {"position": [0, 0], "blocks": [
    {
        "opcode": "(VALUE)",
        "inputs": {
            "VALUE": {"text": "HI"},
        },
        "options": {}
    }
]}

from utility import readJSONFile
#projectData = readJSONFile("btt/project.json", ensurePath=True)

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100
        },
        {
            "name": "Sprite1",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [
                0,
                0
            ],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
            "localVariables": [],
            "localLists": []
        }
    ],
    "globalVariables": [
        {"name": "ZUVOR.MP4", "currentValue": uri, "isCloudVariable": False},
    ],
    "globalLists": [],
    "monitors": [],
    "extensions": [],
    "extensionURLs": {}
}

from pypenguin import validateProject, compressProject
from utility import writeJSONFile, Platform
validateProject(projectData=projectData)
print("[VALIDATION SUCCESS]")
writeJSONFile(filePath="t_source.json", data=projectData, ensurePath=True)
writeJSONFile(filePath="extracted_project/project.json", data=projectData, ensurePath=True)
writeJSONFile(filePath="precompiled.json", data=[], ensurePath=True)
compressProject(
    optimizedProjectDir = "../extracted_project",
    projectFilePath     = "../export.pmp",
    targetPlatform      = Platform.PENGUINMOD,
    deoptimizedDebugFilePath="../t_deop.json",
)
