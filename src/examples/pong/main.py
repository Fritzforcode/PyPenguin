ballCode = {"position": [0,0], "blocks": [
    {"opcode": "when green flag clicked"},
    {
        "opcode": "go to x: (X) y: (Y)",
        "inputs": {
            "X": {"text": "0"},
            "Y": {"text": "0"},
        },
    },
    {
        "opcode": "point in direction (DIRECTION)",
        "inputs": {
            "DIRECTION": {"block": {
                "opcode": "pick random (NUM1) to (NUM2)",
                "inputs": {
                    "NUM1": {"text": "45"},
                    "NUM2": {"text": "135"},
                },
            }},
        },
    },
    {
        "opcode": "set [VARIABLE] to (VALUE)",
        "inputs": {
            "VALUE": {"text": "5"},
        },
        "options": {"VARIABLE": "Speed"},
    },
    {
        "opcode": "forever {BODY}",
        "inputs": {"BODY": {"blocks": [
            {
                "opcode": "move (STEPS) steps",
                "inputs": {
                    "STEPS": {"block": {
                        "opcode": "value of [VARIABLE]",
                        "options": {"VARIABLE": "Speed"},
                    }},
                },
            },
        ]}},
    },
]}


# ['instruction', 'lastInstruction', 'textReporter', 'numberReporter', 'booleanReporter']
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
            "name": "Ball",
            "isStage": False,
            "scripts": [ballCode],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "localVariables": [],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [0,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
        {
            "name": "Player 1",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "localVariables": [],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [0,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
        {
            "name": "Player 2",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "localVariables": [],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [0,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
    ],
    "globalVariables": [
        {
            "name": "Speed",
            "currentValue": "",
            "isCloudVariable": False,
        },
    ],
    "globalLists": [],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "monitors": [],
    "extensionData": {},
    "extensions": [],
}
import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile, pp

validateProject(projectData=projectData)
#pp(projectData)

writeJSONFile(
    filePath = "temp2.json",
    data     = projectData
)

writeJSONFile(
    filePath = "project/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDir = "project",
    projectFilePath     = "export.pmp",
    temporaryDir        = "temporary",
    writeDebugFiles     = True,
)
