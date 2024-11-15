from alu import excecuteAluInstrDef
from utility import readRegisterDef, setRegisterDef

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                excecuteAluInstrDef,
                readRegisterDef,
                setRegisterDef,
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
            "name": "[ALU] return value",
            "currentValue": 0,
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [5,5],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
        {
            "name": "[ALU] Arg A",
            "currentValue": 0,
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [5,50],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
        {
            "name": "[ALU] Arg B",
            "currentValue": 0,
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [5,50],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
        {
            "name": "REGISTERS",
            "currentValue": 7*["0"],
            "monitor": {
                "visible": True,
                "size": [100,250],
                "position": [200,100],
            },
        }
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

import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile

validateProject(projectData=projectData)

writeJSONFile(
    filePath = "../../../project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDirectory = "../../../project",
    projectFilePath           = "../../../export.pmp",
    temporaryDirectory        = "../../../temporary",
    writeDebugFiles           = False,
)
