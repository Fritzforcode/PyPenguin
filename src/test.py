moveDiskDef = {"position": [0,1000], "blocks":[
    {
        "opcode": "define ...",
        "inputs": {},
        "options": {
            "noScreenRefresh": True, 
            "blockType": "instruction", 
            "customOpcode": "move disk from (source) to (target)"
        },
        "comment": None,
    },
    {
        "opcode": "add (ITEM) to [LIST]",
        "inputs": {"ITEM":{
            "mode": "block-and-text",
            "block": {
                "opcode": "join (STRING1) (STRING2) (STRING3)",
                "inputs": {
                    "STRING1": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "inputs": {},
                            "options": {"VALUE": "source"},
                            "comment": None,
                        },
                        "text": "",
                    },
                    "STRING2": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": " --> ",
                    },
                    "STRING3": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "inputs": {},
                            "options": {"VALUE": "target"},
                            "comment": None,
                        },
                        "text": "",
                    },
                },
                "options": {},
                "comment": None,
            },
            "text": "",
        }},
        "options": {"LIST": "LOG"},
        "comment": None,
    },
]}

nEqualsOne = {
    "mode": "block-only",
    "block": {
        "opcode": "(OPERAND1) = (OPERAND2)",
        "inputs": {
            "OPERAND1": {
                "mode": "block-and-text", 
                "block": {
                    "opcode": "value of text argument [VALUE]",
                    "inputs": {},
                    "options": {"VALUE": "n"},
                    "comment": None,
                },
                "text": "",
            },
            "OPERAND2": {"mode": "block-and-text", "block": None, "text": "1"},
        },
        "options": {},
        "comment": None,
    },
}

caseOne = {
    "mode": "script",
    "blocks": [
        {
            "opcode": "call ...",
            "inputs": {
                "source": {
                    "mode": "block-and-text", 
                    "block": {
                        "opcode": "value of text argument [VALUE]",
                        "inputs": {},
                        "options": {"VALUE": "source"},
                        "comment": None,
                    },
                    "text": "",
                },
                "target": {
                    "mode": "block-and-text", 
                    "block": {
                        "opcode": "value of text argument [VALUE]",
                        "inputs": {},
                        "options": {"VALUE": "target"},
                        "comment": None,
                    },
                    "text": "",
                },
            },
            "options": {"customOpcode": "move disk from (source) to (target)"},
            "comment": None,
        },
    ],
}

callOne = {
    "opcode": "call ...",
    "inputs": {
        "n": {
            "mode": "block-and-text",
            "block": {
                "opcode": "(NUM1) - (NUM2)",
                "inputs": {
                    "NUM1": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "inputs": {},
                            "options": {"VALUE": "n"},
                            "comment": None,
                        },
                        "text": "",
                    },
                    "NUM2": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "1",
                    },
                },
                "options": {},
                "comment": None,
            },
            "text": "",
        },
        "source": {
            "mode": "block-and-text",
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "source"},
                "comment": None,
            },
            "text": "",
        },
        "aux": {
            "mode": "block-and-text",
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "target"},
                "comment": None,
            },
            "text": "",
        },
        "target": {
            "mode": "block-and-text",
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "aux"},
                "comment": None,
            },
            "text": "",
        },
    },
    "options": {"customOpcode": "hanoi (n) (source) (aux) (target)"},
    "comment": None,
}

callTwo = {
    "opcode": "call ...",
    "inputs": {
        "source": {
            "mode": "block-and-text", 
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "source"},
                "comment": None,
            },
            "text": "",
        },
        "target": {
            "mode": "block-and-text", 
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "target"},
                "comment": None,
            },
            "text": "",
        },
    },
    "options": {"customOpcode": "move disk from (source) to (target)"},
    "comment": None,
}

callThree = {
    "opcode": "call ...",
    "inputs": {
        "n": {
            "mode": "block-and-text",
            "block": {
                "opcode": "(NUM1) - (NUM2)",
                "inputs": {
                    "NUM1": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "value of text argument [VALUE]",
                            "inputs": {},
                            "options": {"VALUE": "n"},
                            "comment": None,
                        },
                        "text": "",
                    },
                    "NUM2": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "1",
                    },
                },
                "options": {},
                "comment": None,
            },
            "text": "",
        },
        "source": {
            "mode": "block-and-text",
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "aux"},
                "comment": None,
            },
            "text": "",
        },
        "aux": {
            "mode": "block-and-text",
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "source"},
                "comment": None,
            },
            "text": "",
        },
        "target": {
            "mode": "block-and-text",
            "block": {
                "opcode": "value of text argument [VALUE]",
                "inputs": {},
                "options": {"VALUE": "target"},
                "comment": None,
            },
            "text": "",
        },
    },
    "options": {"customOpcode": "hanoi (n) (source) (aux) (target)"},
    "comment": None,
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
        "inputs": {},
        "options": {
            "noScreenRefresh": True, 
            "blockType": "instruction", 
            "customOpcode": "hanoi (n) (source) (aux) (target)"
        },
        "comment": None,
    },
    {
        "opcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
        "inputs": {
            "CONDITION": nEqualsOne,
            "SUBSTACK": caseOne,
            "SUBSTACK2": caseTwo,
        },
        "options": {},
        "comment": None,
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
    filePath = "../project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory = "../project",
    projectFilePath           = "../export.pmp",
    temporaryDirectory        = "../temporary",
    writeDebugFiles           = True,
)

