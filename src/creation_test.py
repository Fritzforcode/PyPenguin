scriptA = {"position": [0, 0], "blocks": [
    {
        "opcode": "broadcast ([MESSAGE]) and wait",
        "inputs": {
            "MESSAGE": {
                "option": [
                    "value",
                    "refresh"
                ]
            }
        },
        "options": {}
    }
]}

from utility import readJSONFile
#projectData = readJSONFile("btt/project.json", ensurePath=True)

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [scriptA],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100
        },
        {
            "name": "Sprite1",
            "isStage": False,
            "scripts": [
                {"position": [0,0], "blocks": [{
                    "opcode": "(VALUE)",
                    "inputs": {"VALUE": {"text": "\n"}},
                }]},
                {"position": [0,0], "blocks": [{
                    "opcode": "(VALUE)",
                    "inputs": {"VALUE": {"text": "\r"}},
                }]},
                {"position": [0,0], "blocks": [{
                    "opcode": "(VALUE)",
                    "inputs": {"VALUE": {"text": chr(13)}},
                }]},
            ],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [
                0,
                0
            ],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
            "localVariables": [],
            "localLists": []
        }
    ],
    "globalVariables": [
        {
            "name": "ADDRESSING",
            "currentValue": "",
            "isCloudVariable": False
        },
        {
            "name": "OPCODES",
            "currentValue": "",
            "isCloudVariable": False
        },
        {
            "name": "BYTEORDER",
            "currentValue": "",
            "isCloudVariable": False
        },
        {
            "name": "PAGE_WRAPPING_BUG",
            "currentValue": "",
            "isCloudVariable": False
        }
    ],
    "globalLists": [],
    "monitors": [],
    "extensions": [
        "jgJSON",
        "lmsTempVars2",
        "Bitwise"
    ],
    "extensionURLs": {
        "Bitwise": "https://extensions.turbowarp.org/bitwise.js"
    }
}

from pypenguin import validateProject, compressProject
from utility import writeJSONFile, Platform
validateProject(projectData=projectData)
print("[VALIDATION SUCCESS]")
writeJSONFile(filePath="t_source.json", data=projectData, ensurePath=True)
#writeJSONFile(filePath="extracted_project/project.json", data=projectData, ensurePath=True)
writeJSONFile(filePath="precompiled.json", data=[], ensurePath=True)
compressProject(
    optimizedProjectDir = "../extracted_project",
    projectFilePath     = "../export.pmp",
    targetPlatform      = Platform.PENGUINMOD,
    deoptimizedDebugFilePath="../t_deop.json",
)
