from src.pypenguin import validateProject, deoptimizeAndCompressProject
from src.pypenguin.helper_functions import writeJSONFile
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/pypenguin')))

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
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {
                                    "mode": "block-and-text",
                                    "block": {
                                        "opcode": "set (KEY) to (VALUE) in (JSON)",
                                        "inputs": {
                                            "KEY": {"mode": "block-and-text", "block": None, "text": "Gandalf"},
                                            "VALUE": {"mode": "block-and-text", "block": {
                            "opcode": "VARIABLE",
                            "inputs": {},
                            "options": {"VARIABLE": "var"},
                            "comment": None,
                        }, "text": "Indiana JONES"},
                                            "JSON": {
                                    "mode": "block-and-text",
                                    "block": {
                                        "opcode": "set (KEY) to (VALUE) in (JSON)",
                                        "inputs": {
                                            "KEY": {"mode": "block-and-text", "block": None, "text": "Bilbo"},
                                            "VALUE": {"mode": "block-and-text", "block": None, "text": "Frodo"},
                                            "JSON": {"mode": "block-and-text", "block": None, "text": "{}"},  
                                        },
                                        "options": {},
                                        "comment": None,
                                    },
                                    "text": "MoinThisValue"
                                },  
                                        },
                                        "options": {},
                                        "comment": None,
                                    },
                                    "text": "MoinThisValue"
                                }
                            },
                            "options": {"VARIABLE": "var"},
                            "comment": None,
                        },
                    ],
                },
            ],
            "comments": [],
            "currentCostume": 0,
            "costumes": [{
                "name": "costume1",
                "dataFormat": "png",
                "fileStem": "b86efb7f23387300cf9037a61f328ab9",
                "bitmapResolution": 2,
                "rotationCenter": [158, 146]
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
        }
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
        }
    }
}
validateProject(projectData=projectData)

writeJSONFile(
    filePath="project/project.json",
    data=projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory="project",
    projectFilePath="export.pmp",
    temporaryDirectory="temporary"
)

