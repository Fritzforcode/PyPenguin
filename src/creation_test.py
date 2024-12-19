scripts = [
{'position': [0, 0],
 'blocks': [{'opcode': 'if <CONDITION> then {THEN} else {ELSE}',
             'inputs': {'CONDITION': {'block': {'opcode': '(OPERAND1) > '
                                                          '(OPERAND2)',
                                                'inputs': {'OPERAND1': {'block': {'opcode': 'value '
                                                                                            'of '
                                                                                            '[VARIABLE]',
                                                                                  'inputs': {},
                                                                                  'options': {'VARIABLE': ['variable',
                                                                                                           'score']}},
                                                                        'text': ''},
                                                           'OPERAND2': {'block': None,
                                                                        'text': '50'}},
                                                'options': {}}},
                        'THEN': {'blocks': [{'opcode': 'say (MESSAGE) for '
                                                       '(SECONDS) seconds',
                                             'inputs': {'MESSAGE': {'block': None,
                                                                    'text': 'You '
                                                                            'win!'},
                                                        'SECONDS': {'block': None,
                                                                    'text': '2'}},
                                             'options': {}}]},
                        'ELSE': {'blocks': [{'opcode': 'say (MESSAGE) for '
                                                       '(SECONDS) seconds',
                                             'inputs': {'MESSAGE': {'block': None,
                                                                    'text': 'Game '
                                                                            'over!'},
                                                        'SECONDS': {'block': None,
                                                                    'text': '2'}},
                                             'options': {}}]}},
             'options': {}},
            {'opcode': 'delete all of [LIST]',
             'inputs': {},
             'options': {'LIST': ['list', 'players']}}]}
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
                    "currentValue": "www",
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
            "name": "score",
            "currentValue": "Günter Jüchen",
            "isCloudVariable": True,
        },
        {
            "name": "timer",
            "currentValue": "",
            "isCloudVariable": False,
        },
        {
            "name": "go to",
            "currentValue": "",
            "isCloudVariable": False,
        },
        {
            "name": "points",
            "currentValue": "",
            "isCloudVariable": False,
        },
        
        {
            "name": "var",
            "currentValue": "",
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
        {"name": "players", "currentValue": []},
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

extractAndOptimizeProject(
    projectFilePath        = "export.pmp",
    optimizedProjectDir    = "project",
    temporaryDir           = "temporary",
    optimizedDebugFilePath = "t_finished.json"
)
