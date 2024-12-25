scripts = [
    {"position": [0,0], "blocks": [
        {
            "opcode": "call custom block",
            "inputs": {
                "f": {"block": {
                    "opcode": "call custom block",
                    "inputs": {},
                    "options": {"customOpcode": ["value", ""]},
                }},
            },
            "options": {"customOpcode": ["value", "abcease <f>"]},
        },
    ]},
    {"position": [500, 0], "blocks": [
        {
            "opcode": "define custom block",
            "options": {
                "noScreenRefresh": ["value", True],
                "blockType": ['value', 'instruction'],
                "customOpcode": ["value", "abcease <f>"],
            }
        },
        {
            "opcode": "define custom block",
            "options": {
                "noScreenRefresh": ["value", True],
                "blockType": ['value', 'instruction'],
                "customOpcode": ["value", "bolli"],
            }
        },
    ]},
]
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
            "volume": 100,
        },
        {
            "name": "Sprite1",
            "isStage": False,
            "scripts": scripts,
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [
                {
                    "name": "pop",
                    "extension": "wav",
                    "rate": 48000,
                    "sampleCount": 1123,
                },
            ],
            "localVariables": [
                {
                    "name": "loc var",
                    "currentValue": "",
                }
            ],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [77,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
        {
            "name": "Sprite2",
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
            "name": "score",
            "currentValue": "Günter Jüchen",
            "isCloudVariable": True,
        },
        {
            "name": "arg0",
            "currentValue": "",
            "isCloudVariable": False,
        },
        {
            "name": "value1",
            "currentValue": "",
            "isCloudVariable": False,
        },
        
        {
            "name": "register map",
            "currentValue": "",
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
        {"name": "registers", "currentValue": []},
        {"name": "points", "currentValue": []},
    ],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "monitors": [],
 
    "extensionData": {},
    "extensions": ["jgJSON"],
}

from pypenguin import validateProject, deoptimizeAndCompressProject, extractAndOptimizeProject
from pypenguin.helper_functions import writeJSONFile, pp

validateProject(projectData=projectData)
#pp(projectData)

writeJSONFile(
    filePath = "t_source.json",
    data     = projectData
)

writeJSONFile(
    filePath = "project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDir = "project",
    projectFilePath     = "export.pmp",
    temporaryDir        = "temporary",
    deoptimizedDebugFilePath="t_deop.json",
)
#
#extractAndOptimizeProject(
#    projectFilePath        = "export.pmp",
#    optimizedProjectDir    = "project",
#    temporaryDir           = "temporary",
#    optimizedDebugFilePath = "t_finished.json"
#)
