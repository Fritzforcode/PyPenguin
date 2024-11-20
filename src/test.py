A = {
    "position": [0,0],
    "blocks": [
        {
            "opcode": "create clone of [TARGET]",
            "options": {"TARGET": "sPrITe"},
        },
    ],
}
projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                A,   
            ],
            "comments": [],
            "currentCostume": 0,
            "costumes": [{
                "name": "costume1",
                "dataFormat": "png",
                "fileStem": "b86efb7f23387300cf9037a61f328ab9",
                "bitmapResolution": 2,
                "rotationCenter": [158, 146],
                }],
            "sounds": [],
            "volume": 100,
        },
        {
            "name": "sPrITe",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [{
                "name": "costume1",
                "dataFormat": "png",
                "fileStem": "b86efb7f23387300cf9037a61f328ab9",
                "bitmapResolution": 2,
                "rotationCenter": [158, 146],
            }],
            "sounds": [],
            "volume": 100,
            "localVariables": [],
            "localLists": [],
            "layerOrder": 1,
            "visible": True,
            "position": [100, 100],
            "size": 100,
            "direction": 0,
            "draggable": True,
            "rotationStyle": "all around",
        },
    ],
    "globalVariables": [
        {
            "name": "var",
            "currentValue": 33,
            "monitor": None,
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
        {
            "name": "LOG",
            "currentValue": [],
            "monitor": None
        },
    ],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "extensionData": {},
    "extensions": ["jgJSON"],
    "meta": {
        "semver": "3.0.0",
        "vm": "0.2.0",
        "agent": "",
        "platform": {
            "name": "PenguinMod",
            "url": "https://penguinmod.com/",
            "version": "stable"
        },
    },
}

from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile, pp

validateProject(projectData=projectData)

writeJSONFile(
    filePath = "../project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory = "../project",
    projectFilePath           = "../export.pmp",
    temporaryDirectory        = "../temporary",
    writeDebugFiles           = True,
)
