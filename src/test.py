from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                {
                    "position": [0,0],
                    "blocks": [
                        {
                            "opcode": "define ...",
                            "inputs": {},
                            "options": {"blockType": "instruction", "noScreenRefresh": False, "customOpcode": "interpret (node)"},
                            "comment": None,
                        },
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {
                                    "mode": "block-and-text", 
                                    "block": {
                                        "opcode": "value of text argument (VALUE)",
                                        "inputs": {},
                                        "options": {"VALUE": "node"},
                                        "comment": None,
                                    }, 
                                    "text": ""}
                                },
                            "options": {"VARIABLE": "node"},
                            "comment": None,
                        },
                        {
                            "opcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
                            "inputs": {
                                "CONDITION": {
                                    "mode": "block-only", 
                                    "block": {
                                        "opcode": "(OPERAND1) = (OPERAND2)", 
                                        "inputs": {
                                            "OPERAND1": {
                                                "mode": "block-and-text", 
                                                "block": {
                                                    "opcode": "value of (VARIABLE)",
                                                    "inputs": {},
                                                    "options": {"VARIABLE": "node"},
                                                    "comment": None,
                                                }, 
                                                "text": ""
                                            },
                                            "OPERAND2": {"mode": "block-and-text", "block": None, "text": "Module"}, 
                                        }, 
                                        "options":{}, 
                                        "comment":None
                                    }
                                },
                                
                            },
                            "options": {},
                            "comment": None,
                        },
                        
                    ],
                },
                {
                    "position": [0, 800],
                    "blocks": [
                        {
                            "opcode": "case (CONDITION) {SUBSTACK}",
                            "inputs": {
                                "CONDITION": {
                                    "mode": "block-and-text",
                                    "block": None,
                                    "text": "belloHello",
                                },
                                "SUBSTACK": {
                                    "mode": "script",
                                    "blocks": [
                                        7
                                    ],
                                },
                            },
                            "options": {},
                            "comment": None,
                        },
                    ],
                }
                
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
            "name": "node",
            "currentValue": 33,
            "monitor": None,
            "isCloudVariable": False,
        },
    ],
    "globalLists": [],
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

validateProject(projectData=projectData)

writeJSONFile(
    filePath="../project/project.json",
    data=projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory="../project",
    projectFilePath="../export.pmp",
    temporaryDirectory="../temporary",
    writeDebugFiles=True,
)

