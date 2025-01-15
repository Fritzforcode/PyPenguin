from alu import excecuteAluInstrDef
from utility import readRegisterDef, setRegisterDef
from control import executeCurrentInstrDef, programm, executeControlInstrDef

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                executeCurrentInstrDef,
                excecuteAluInstrDef,
                executeControlInstrDef,
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
            "name": "current instr",
            "currentValue": "",
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [215,0],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
        {
            "name": "PROGRAMM COUNTER",
            "currentValue": 1,
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [0,0],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
        {
            "name": "NEW PC",
            "currentValue": 1,
            "monitor": {
                "visible": True,
                "size": [20,70],
                "position": [0,20],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
        {
            "name": "[CRTL] condition met?",
            "currentValue": 0,
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [0,145],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
        {
            "name": "[ALU] return value",
            "currentValue": 0,
            "monitor": {
                "visible": True,
                "size": [20,10],
                "position": [0,95],
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
                "position": [0,55],
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
                "position": [0,75],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": True,
            },
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
        {
            "name": "PROGRAMM",
            "currentValue": programm,
            "monitor": {
                "visible": True,
                "size": [150,250],
                "position": [300,100],
            },
        },
        {
            "name": "REGISTERS",
            "currentValue": 7*["0"],
            "monitor": {
                "visible": True,
                "size": [100,250],
                "position": [200,100],
            },
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

import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.utility import writeJSONFile

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
