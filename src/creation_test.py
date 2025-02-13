scriptA = {"position": [0, 0], "blocks": [
    {
        "opcode": "set runtime var (VARIABLE) to (VALUE)",
        "inputs": {
            "VARIABLE": {"text": "ABc"},
            "VALUE": {"block": {
                "opcode": "new line"
            }},
        },
    },
]}


projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
        },
        {"name": "Sprite123", "isStage": False, "scripts": [scriptA], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100, "layerOrder": 1, "visible": True, "position": [0,0], "size": 100, "direction": 90, "draggable": True, "rotationStyle": "all around", 
        "localVariables": [{"name": "locVar", "currentValue": ""}], "localLists": [{"name": "locList", "currentValue": []}],
        },
    ],
    "globalVariables": [{"name": "globVar", "currentValue": "", "isCloudVariable": False}],
    "globalLists": [{"name": "globList", "currentValue": []}],
    "monitors": [],
    "extensions": [],
}

from pypenguin import validateProject, compressProject
from pypenguin.utility import writeJSONFile, Platform
validateProject(projectData=projectData)
print("[VALIDATION SUCCESS]")
writeJSONFile(filePath="t_source.json", data=projectData)
writeJSONFile(filePath="extracted_project/project.json", data=projectData)
writeJSONFile(filePath="precompiled.json", data=[])
compressProject(
    optimizedProjectDir = "extracted_project",
    projectFilePath     = "export.pmp",
    targetPlatform      = Platform.PENGUINMOD,
    deoptimizedDebugFilePath="t_deop.json",
)
