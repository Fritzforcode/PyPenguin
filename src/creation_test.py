scripts = [
{   'position': [0, 0],
    'blocks': [   {   '_type': 'BLOCK',
                      'opcode': 'call custom block',
                      'inputs': {   'value': {   'block': {   '_type': 'BLOCK',
                                                              'opcode': '(OPERAND1) '
                                                                        '+ '
                                                                        '(OPERAND2)',
                                                              'inputs': {   'OPERAND1': {   'text': '4'},
                                                                            'OPERAND2': {   'block': {   '_type': 'BLOCK',
                                                                                                         'opcode': '(OPERAND1) '
                                                                                                                   '* '
                                                                                                                   '(OPERAND2)',
                                                                                                         'inputs': {   'OPERAND1': {   'text': '3'},
                                                                                                                       'OPERAND2': {   'text': '5'}}}}}}}},
                      'options': {'customOpcode': ['value', 'VOID (value)']}}]},
    {
        "position": [500, 0],
        "blocks": [
            {
                "opcode": "define custom block",
                "options": {
                    "noScreenRefresh": ["value", True], 
                    "blockType": ["value", "instruction"], 
                    "customOpcode": ["value", "VOID (value)"],
                },
            },
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {"VALUE": {"block": {
                    "opcode": "value of text [ARGUMENT]",
                    "options": {"ARGUMENT": ["value", "value"]},
                }}},
                "options": {"VARIABLE": ["variable", "__VOID__"]},
            },
        ]
    },
]
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
            "name": "Sprite1",
            "isStage": False,
            "scripts": scripts,
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [
                {
                    "name": "pop",
                    "extension": "wav",
                    "rate": 48000,
                    "sampleCount": 1123,
                },
            ],
            "localVariables": [
                {
                    "name": "loc var",
                    "currentValue": "",
                }
            ],
            "localLists": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [77,0],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
        },
        {
            "name": "Sprite2",
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
            "name": "__VOID__",
            "currentValue": "",
            "isCloudVariable": True,
        },
    ],
    "globalLists": [
        {"name": "registers", "currentValue": []},
        {"name": "points", "currentValue": []},
    ],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "monitors": [],
 
    "extensionData": {},
    "extensions": ["jgJSON"],
}

from pypenguin import validateProject, deoptimizeAndCompressProject, extractAndOptimizeProject
from pypenguin.helper_functions import writeJSONFile, pp

validateProject(projectData=projectData)
#pp(projectData)

print("[VALIDATION SUCCESS]")

writeJSONFile(
    filePath = "t_source.json",
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
    deoptimizedDebugFilePath="t_deop.json",
)
#
#extractAndOptimizeProject(
#    projectFilePath        = "export.pmp",
#    optimizedProjectDir    = "project",
#    temporaryDir           = "temporary",
#    optimizedDebugFilePath = "t_finished.json"
#)
