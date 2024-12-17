scripts = [
{'position': [0, 0],
 'blocks': [{'opcode': 'when green flag clicked', 'inputs': {}, 'options': {}},
            {'opcode': 'set [VARIABLE] to (VALUE)',
             'inputs': {'VALUE': {'block': None, 'text': '0'}},
             'options': {'VARIABLE': ["variable", "score"]}},
            {'opcode': 'set [VARIABLE] to (VALUE)',
             'inputs': {'VALUE': {'block': None, 'text': '10'}},
             'options': {'VARIABLE': ["variable", "timer"]}},
            {'opcode': 'add (ITEM) to [LIST]',
             'inputs': {'ITEM': {'block': None, 'text': 'Player 1'}},
             'options': {'LIST': ["list", "players"]}},
            {'opcode': 'delete all of [LIST]',
             'inputs': {},
             'options': {'LIST': ["list", "points"]}},
            {'opcode': 'ask (QUESTION) and wait',
             'inputs': {'QUESTION': {'block': None,
                                     'text': 'What is your name?'}},
             'options': {}},
            {'opcode': 'say (MESSAGE) for (SECONDS) seconds',
             'inputs': {'MESSAGE': {'block': {'opcode': 'join (STRING1) '
                                                        '(STRING2)',
                                              'inputs': {'STRING1': {'block': None,
                                                                     'text': 'Hello, '},
                                                         'STRING2': {'block': {'opcode': 'answer',
                                                                               'inputs': {},
                                                                               'options': {}},
                                                                     'text': ''}},
                                              'options': {}},
                                    'text': ''},
                        'SECONDS': {'block': None, 'text': '2'}},
             'options': {}},
            {'opcode': 'broadcast ([MESSAGE])',
             'inputs': {'MESSAGE': {'block': None, 'option': 'start game'}},
             'options': {}},
            {'opcode': 'create clone of ([TARGET])',
             'inputs': {'TARGET': {'block': None, 'option': ["myself", "myself"]}},
             'options': {}},
            {'opcode': 'play sound ([SOUND]) until done',
             'inputs': {'SOUND': {'block': None, 'option': ["sound", "pop"]}},
             'options': {}}]}
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
                    "monitor": None,
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
            "name": "Sprite6",
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