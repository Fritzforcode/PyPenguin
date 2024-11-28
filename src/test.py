A = [
    {
        "position": [0,0],
        "blocks": [
            {
                "opcode": "create clone of [TARGET]",
                "inputs": {
                    "TARGET": {
                        "mode": "block-and-option",
                        "block": None,
                        "option": "Shoutout to @ddededodediamante! 👍",
                    },
                },
            },
        ],
    },
]
projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": A,
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
        },
        {
            "name": "Sprite1",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "localVariables": [],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [0,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
        {
            "name": "Sprite6",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "localVariables": [],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [0,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
    ],
    "globalVariables": [
        {
            "name": "var",
            "currentValue": "",
            "monitor": None,
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
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
#pp(projectData)

writeJSONFile(
    filePath = "temp2.json",
    data     = projectData
)

writeJSONFile(
    filePath = "project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory = "project",
    projectFilePath           = "export.pmp",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)
