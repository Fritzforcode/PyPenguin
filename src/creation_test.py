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
        {
            "name": "t",
            "isStage": False,
            "scripts": [
                {
                    "position": [0, 0],
                    "blocks"  : [
                        {
                            "opcode": "length of (TEXT)"
                        }
                    ],
                }
            ],
            "comments": [{"position": [8, 9], "size": [52, 32], "isMinimized": True, "text": "hi"}],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 99,
            "layerOrder": 5,
            "visible": True,
            "position": [0, 0],
            "size": 100,
            "direction": 0,
            "draggable": True,
            "rotationStyle": "left-right",
            "localVariables": [],
            "localLists": [],
        },
    ],
    "globalVariables": [],
    "globalLists": [],
    "monitors": [],
    "extensions": [""],
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
    projectFilePath     = "export.sb3",
    temporaryDir        = "temporary",
    targetPlatform      = Platform.PENGUINMOD,
    deoptimizedDebugFilePath="t_deop.json",
)