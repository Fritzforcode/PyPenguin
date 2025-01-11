script = {"position": [0, 0], "blocks": [
    {
        "opcode": "ask (QUESTION) and wait",
        "inputs": {
            "QUESTION": {"block": {
                "opcode": "value of [VARIABLE]",
                "options": {"VARIABLE": ["variable", "globVar"]}
            }},
        },
    },
    {
        "opcode": "if <CONDITION> then {THEN}",
        "inputs": {
            "CONDITION": {"block": {
                "opcode": "(OPERAND1) = (OPERAND2)",
                "inputs": {"OPERAND1": {"text": "5"}, "OPERAND2": {"text": "-6"}},
            }},
            "THEN": {"blocks": [
                {
                    "opcode": "say (MESSAGE)",
                    "inputs": {"MESSAGE": {"block": {
                        "opcode": "value of [VARIABLE]",
                        "options": {"VARIABLE": ["variable", "locVar"]},
                    }}},
                },
                {
                    "opcode": "change [VARIABLE] by (VALUE)",
                    "inputs": {"VALUE": {"text": "33"}},
                    "options": {"VARIABLE": ["variable", "locVar"]},
                },
            ]},
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
        {"name": "Sprite123", "isStage": False, "scripts": [script], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100, "layerOrder": 1, "visible": True, "position": [0,0], "size": 100, "direction": 90, "draggable": True, "rotationStyle": "all around", 
        "localVariables": [{"name": "locVar", "currentValue": ""}], "localLists": [{"name": "locList", "currentValue": []}],
        },
    ],
    "globalVariables": [{"name": "globVar", "currentValue": "", "isCloudVariable": False}],
    "globalLists": [{"name": "globList", "currentValue": []}],
    "monitors": [],
    "extensions": [],
}
#TODO sprites[1].name

from pypenguin import validateProject, deoptimizeAndCompressProject, extractAndOptimizeProject
from pypenguin.helper_functions import writeJSONFile, pp, Platform
validateProject(projectData=projectData)
print("[VALIDATION SUCCESS]")
writeJSONFile(filePath="t_source.json", data=projectData)
writeJSONFile(filePath="project/project.json", data=projectData)
deoptimizeAndCompressProject(
    optimizedProjectDir = "project",
    projectFilePath     = "export.pmp",
    temporaryDir        = "temporary",
    targetPlatform      = Platform.PENGUINMOD,
    deoptimizedDebugFilePath="t_deop.json",
)