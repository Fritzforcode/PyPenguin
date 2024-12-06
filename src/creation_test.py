A = [
    {
        "position": [0, 0],
        "blocks": [
            {
                "opcode": "define custom block",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "instruction",
                    "customOpcode": "instr (num txt) <bool val> !"
                }
            },
            {
                "opcode": "return (VALUE)",
                "inputs": {"VALUE": {}},
            },
        ]
    },
    {
        "position": [0, 100],
        "blocks": [
            {
                "opcode": "define custom block",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "lastInstruction",
                    "customOpcode": "lastInstr (txt) <bool val>!"
                }
            }
        ]
    },
    {
        "position": [0, 200],
        "blocks": [
            {
                "opcode": "define custom block",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "textReporter",
                    "customOpcode": "reportText (txt)"
                }
            }
        ]
    },
    {
        "position": [0, 300],
        "blocks": [
            {
                "opcode": "define custom block",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "numberReporter",
                    "customOpcode": "reportNumber (num)"
                }
            }
        ]
    },
    {
        "position": [0, 400],
        "blocks": [
            {
                "opcode": "define custom block",
                "options": {
                    "noScreenRefresh": False,
                    "blockType": "booleanReporter",
                    "customOpcode": "reportBool <bool>"
                }
            }
        ]
    }
]

# ['instruction', 'lastInstruction', 'textReporter', 'numberReporter', 'booleanReporter']
projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": A,
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
        },
        {
            "name": "Sprite1",
            "isStage": False,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
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
            "name": "c",
            "currentValue": "Günter Jüchen",
            "isCloudVariable": True,
        },
        {
            "name": "var",
            "currentValue": "",
            "isCloudVariable": False,
        },
    ],
    "globalLists": [
        {"name": "list", "currentValue": []},
    ],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
#['x position', 'y position', 'direction', 'bubble width', 'bubble height', 'x stretch', 'y stretch', 
# '[EFFECT] sprite effect', 'tint color', 'visible?', 'layer', 'costume [PROPERTY]', 'backdrop [PROPERTY]', 'size', 
# '[EFFECT] sound effect', 'volume', 'answer', 'mouse down?', 'mouse clicked?', 'mouse x', 'mouse y', 
# 'clipboard item', 'draggable?', 'loudness', 'loud?', 'timer', 'current [PROPERTY]', 'days since 2000', 'username', 'logged in?', 'value of [VARIABLE]', 'value of [LIST]']
    "monitors": [
 #{'opcode': 'clipboard item',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'draggable?',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'loudness',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'loud?',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'timer',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
#
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "YEAR"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "MONTH"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "DATE"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "DAYOFWEEK"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "HOUR"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "MINUTE"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "SECOND"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'current [PROPERTY]',
 # 'options': {"PROPERTY": "TIMESTAMP"},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
#
#
 #{'opcode': 'days since 2000',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'username',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'logged in?',
 # 'options': {},
 # 'position': [10, 10],
 # 'spriteName': 'Sprite1',
 # 'visible': True},
 #{'opcode': 'value of [VARIABLE]',
 # 'options': {"VARIABLE": "var"},
 # 'position': [10, 10],
 # 'spriteName': None,
 # 'visible': True,
 # "sliderMin": 0,
 # "sliderMax": 100,
 # "onlyIntegers": True,
 #},
 #{'opcode': 'value of [VARIABLE]',
 # 'options': {"VARIABLE": "loc var"},
 # 'position': [10, 10],
 # 'spriteName': "Sprite1",
 # 'visible': True,
 # "sliderMin": 0,
 # "sliderMax": 100,
 # "onlyIntegers": True,
#},
 {'opcode': 'value of [LIST]',
  'options': {"LIST": "list"},
  'position': [10, 10],
  'spriteName': None,
  'visible': True,
  "size": [0,0],
  }
 ],
 
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
