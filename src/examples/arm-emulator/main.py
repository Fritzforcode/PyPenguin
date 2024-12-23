from exec_instr import executeInstr
from utility import *
import json

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                setRegister,
                getRegister,
                setMemory,
                getMemory,
                getKeyElseDefault,
                executeInstr,
            ],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
        },
    ],
    "globalVariables": [
        {
            "name": "register map",
            "currentValue": json.dumps({"r0": 0, "zero": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8, "r9": 9, "sb": 9, "r10": 10, "sl": 10, "r11": 11, "fp": 11, "r12": 12, "ip": 12, "r13": 13, "sp": 13, "r14": 14, "lr": 14, "r15": 15, "pc": 15}),
            "isCloudVariable": False,
        },
        {
            "name": "memory",
            "currentValue": "{}",
            "isCloudVariable": False,
        },
        {
            "name": "flags",
            "currentValue": json.dumps({"zero": False, "negative": False}),
            "isCloudVariable": False,
        },
        *[{"name": name, "currentValue": "", "isCloudVariable": False} for name in ["instr", "instr type", "arg0", "arg1", "arg2", "value1", "value2", "result", "address"]],
    ],
    "globalLists": [
        {
            "name": "registers",
            "currentValue": 16*[0],
        },
    ],
    "monitors": [],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "extensionData": {},
    "extensions": ["jgJSON", "Bitwise"],
    "extensionURLs": {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"},
} # L was here

import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile

validateProject(projectData=projectData)

writeJSONFile(
    filePath = "project/project.json",
    data     = projectData
)

writeJSONFile(
    filePath = "temp2.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDir      = "project",
    projectFilePath          = "export.pmp",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp_wrong.json",
)
