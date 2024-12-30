
projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
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
            "name": "program counter",
            "currentValue": "0",
            "isCloudVariable": False,
        },
        *[{"name": name, "currentValue": "", "isCloudVariable": False} for name in ["instr", "instr type", "arg0", "arg1", "arg2", "value1", "value2", "result", "address", "do branch", "target pc", "current instruction"]],
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
