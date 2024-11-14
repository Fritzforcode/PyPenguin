moveDiskDef = {"position": [0,1000], "blocks":[
    {
        "opcode": "define ...",
        "options": {
            "noScreenRefresh": True, 
            "blockType": "instruction", 
            "customOpcode": "move disk from (source) to (target)"
        },
    },
    {
        "opcode": "add (ITEM) to [LIST]",
        "inputs": {"ITEM":{
            "block": {
                "opcode": "join (STRING1) (STRING2) (STRING3)",
                "inputs": {
                    "STRING1": {
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "source"},
                        },
                    },
                    "STRING2": {"text": " --> "},
                    "STRING3": {
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "target"},
                        },
                    },
                },
            },
        }},
        "options": {"LIST": "LOG"},
    },
]}

nEqualsOne = {
    "block": {
        "opcode": "(OPERAND1) = (OPERAND2)",
        "inputs": {
            "OPERAND1": {
                "block": {
                    "opcode": "value of text argument [VALUE]",
                    "options": {"VALUE": "n"},
                },
            },
            "OPERAND2": {"text": "1"},
        },
    },
}

caseOne = {
    "mode": "script",
    "blocks": [
        {
            "opcode": "call ...",
            "inputs": {
                "source": {
                    "block": {
                        "opcode": "value of text argument [VALUE]",
                        "options": {"VALUE": "source"},
                    },
                },
                "target": {
                    "block": {
                        "opcode": "value of text argument [VALUE]",
                        "options": {"VALUE": "target"},
                    },
                },
            },
            "options": {"customOpcode": "move disk from (source) to (target)"},
        },
    ],
}

callOne = {
    "opcode": "call ...",
    "inputs": {
        "n": {
            "block": {
                "opcode": "(NUM1) - (NUM2)",
                "inputs": {
                    "NUM1": {
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "n"},
                        },
                    },
                    "NUM2": {
                        "text": "1",
                    },
                },
            },
        },
        "source": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "source"},
            },
        },
        "aux": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "target"},
            },
        },
        "target": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "aux"},
            },
        },
    },
    "options": {"customOpcode": "hanoi (n) (source) (aux) (target)"},
}

callTwo = {
    "opcode": "call ...",
    "inputs": {
        "source": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "source"},
            },
        },
        "target": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "target"},
            },
        },
    },
    "options": {"customOpcode": "move disk from (source) to (target)"},
}

callThree = {
    "opcode": "call ...",
    "inputs": {
        "n": {
            "block": {
                "opcode": "(NUM1) - (NUM2)",
                "inputs": {
                    "NUM1": {
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "n"},
                        },
                    },
                    "NUM2": {"text": "1"},
                },
            },
        },
        "source": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "aux"},
            },
        },
        "aux": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "source"},
            },
        },
        "target": {
            "block": {
                "opcode": "value of text argument [VALUE]",
                "options": {"VALUE": "target"},
            },
        },
    },
    "options": {"customOpcode": "hanoi (n) (source) (aux) (target)"},
}

caseTwo = {
    "mode": "script",
    "blocks": [
        callOne,
        callTwo,
        callThree, 
    ],
}

hanoiDef = {"position": [0,0], "blocks": [
    {
        "opcode": "define ...",
        "options": {
            "noScreenRefresh": True, 
            "blockType": "instruction", 
            "customOpcode": "hanoi (n) (source) (aux) (target)"
        },
    },
    {
        "opcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
        "inputs": {
            "CONDITION": nEqualsOne,
            "SUBSTACK": caseOne,
            "SUBSTACK2": caseTwo,
        },
    },
]}

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                hanoiDef,
                moveDiskDef,   
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
    ],
    "globalVariables": [
        {
            "name": "var",
            "currentValue": 33,
            "monitor": None,
            "isCloudVariable": False,
        },
        {
            "name": "interpret: node",
            "currentValue": 0,
            "monitor": None,
            "isCloudVariable": False,
        },
        {
            "name": "interpret: i",
            "currentValue": 0,
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
from pypenguin.helper_functions import writeJSONFile

validateProject(projectData=projectData)

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
