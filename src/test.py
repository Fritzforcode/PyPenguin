from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile

interpretDef = {
    "position": [0,0],
    "blocks": [
        {
            "opcode": "define ...",
            "inputs": {},
            "options": {"blockType": "stringReporter", "noScreenRefresh": False, "customOpcode": "interpret (node)"},
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
            "options": {"VARIABLE": "interpret: node"},
            "comment": None,
        },
        {
            "opcode": "switch (CONDITION) {SUBSTACK}",
            "inputs": {
                "CONDITION": {
                    "mode": "block-and-text",
                    "block": {
                        "opcode": "get (VALUE) from (JSON)",
                        "inputs": {
                            "VALUE": {
                                "mode": "block-and-text",
                                "block": None,
                                "text": "_type",
                            },
                            "JSON": {
                                "mode": "block-and-text",
                                "block": {
                                    "opcode": "value of (VARIABLE)", 
                                    "inputs": {}, 
                                    "options": {"VARIABLE": "interpret: node"}, 
                                    "comment": None,
                                },
                                "text": "",
                            },
                        },
                        "options": {},
                        "comment": None,
                    },
                    "text": "",
                },
                "SUBSTACK": {
                    "mode": "script",
                    "blocks": [
                        {
                            "opcode": "case (CONDITION) {SUBSTACK}",
                            "inputs": {
                                "CONDITION": {"mode": "block-and-text", "block": None, "text": "Module"},
                                "SUBSTACK": {
                                    "mode": "script",
                                    "blocks": [
                                        {
                                            "opcode": "set [VARIABLE] to (VALUE)",
                                            "inputs": {"VALUE": {"mode": "block-and-text", "block": None, "text": "0"}},
                                            "options": {"VARIABLE": "interpret: i"},
                                            "comment": None,
                                        }
                                    ],
                                },
                            },
                            "options": {},
                            "comment": None,
                        },
                        {
                            "opcode": "repeat (TIMES) {SUBSTACK}",
                            "inputs": {
                                "TIMES": {"mode": "block-and-text", "block": None, "text": "44"},
                            },
                            "options": {},
                            "comment": None,
                        }
                    ],
                },
                
            },
            "options": {},
            "comment": None,
        },
    ],
}

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                interpretDef,   
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
    filePath = "project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory = "project",
    projectFilePath           = "export.pmp",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)

