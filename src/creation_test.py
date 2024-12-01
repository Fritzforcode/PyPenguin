A = [
    {
        "position": [0, 0],
        "blocks": [
            {
                "opcode": "define ...",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "instruction",
                    "customOpcode": "instr (num txt) <bool val> !"
                }
            }
        ]
    },
    {
        "position": [0, 100],
        "blocks": [
            {
                "opcode": "define ...",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "lastInstruction",
                    "customOpcode": "lastInstr (txt) <bool val>!"
                }
            }
        ]
    },
    {
        "position": [0, 200],
        "blocks": [
            {
                "opcode": "define ...",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "textReporter",
                    "customOpcode": "reportText (txt)"
                }
            }
        ]
    },
    {
        "position": [0, 300],
        "blocks": [
            {
                "opcode": "define ...",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "numberReporter",
                    "customOpcode": "reportNumber (num)"
                }
            }
        ]
    },
    {
        "position": [0, 400],
        "blocks": [
            {
                "opcode": "define ...",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "booleanReporter",
                    "customOpcode": "reportBool <bool>"
                }
            }
        ]
    }
]

# ['instruction', 'lastInstruction', 'textReporter', 'numberReporter', 'booleanReporter']
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
            "localVariables": [
                {
                    "name": "loc var",
                    "currentValue": "",
                    "monitor": None,
                }
            ],
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
    optimizedProjectDir = "project",
    projectFilePath     = "export.pmp",
    temporaryDir        = "temporary",
    writeDebugFiles     = True,
)
