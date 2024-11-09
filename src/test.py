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
                    "blocks": [{
                        "opcode": "define ...",
                        "inputs": {},
                        "options": {"noScreenRefresh": False, "blockType": "instruction"},
                        "segments": [{"type": "label", "text": "wasd"}, {"type": "textInput", "name": "nnm"}],
                        "comment": None
                    }, {
                        "opcode": "set [VARIABLE] to (VALUE)",
                        "inputs": {"VALUE": {"mode":"block-and-text", "block": None, "text": "123"}},
                        "options": {"VARIABLE": "var"},
                        "comment": None
                    }]},
                {
                    "position": [100,0],
                    "blocks": [{
                        "opcode": "define ...",
                        "inputs": {},
                        "options": {"noScreenRefresh": False, "blockType": "lastInstruction"},
                        "segments": [{"type": "label", "text": "wasd"}, {"type": "textInput", "name": "nnm"}],
                        "comment": None
                    }]},
                {
                    "position": [200,0],
                    "blocks": [{
                        "opcode": "define ...",
                        "inputs": {},
                        "options": {"noScreenRefresh": False, "blockType": "stringReporter"},
                        "segments": [{"type": "label", "text": "wasd"}, {"type": "textInput", "name": "nnm"}],
                        "comment": None
                    }]},
                {
                    "position": [300,0],
                    "blocks": [{
                        "opcode": "define ...",
                        "inputs": {},
                        "options": {"noScreenRefresh": False, "blockType": "numberReporter"},
                        "segments": [{"type": "label", "text": "wasd"}, {"type": "textInput", "name": "nnm"}],
                        "comment": None
                    }]},
                {
                    "position": [400,0],
                    "blocks": [{
                        "opcode": "define ...",
                        "inputs": {},
                        "options": {"noScreenRefresh": False, "blockType": "booleanReporter"},
                        "segments": [{"type": "label", "text": "wasd"}, {"type": "textInput", "name": "nnm"}],
                        "comment": None
                    }]},
                
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
    temporaryDirectory="../temporary"
)

