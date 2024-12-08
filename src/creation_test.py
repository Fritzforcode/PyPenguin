A = [
    {
        "position": [
            10,
            10
        ],
        "blocks": [
            {
                "opcode": "when green flag clicked",
                "inputs": {},
                "options": {}
            },
            {
                "opcode": "ask (QUESTION) and wait",
                "inputs": {
                    "QUESTION": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "Enter first number:"
                    }
                },
                "options": {}
            },
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "answer"
                        },
                        "text": ""
                    }
                },
                "options": {
                    "VARIABLE": "firstNumber"
                }
            },
            {
                "opcode": "ask (QUESTION) and wait",
                "inputs": {
                    "QUESTION": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "Enter second number:"
                    }
                },
                "options": {}
            },
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "answer"
                        },
                        "text": None
                    }
                },
                "options": {
                    "VARIABLE": "secondNumber"
                }
            },
            {
                "opcode": "ask (QUESTION) and wait",
                "inputs": {
                    "QUESTION": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "Enter operation (+, -, *, /):"
                    }
                },
                "options": {}
            },
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": {
                            "opcode": "answer"
                        },
                        "text": None
                    }
                },
                "options": {
                    "VARIABLE": "operation"
                }
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {
                        "mode": "block-only",
                        "block": {
                            "opcode": "(OPERAND1) = (OPERAND2)",
                            "inputs": {
                                "OPERAND1": {
                                    "mode": "block-and-text",
                                    "block": {
                                        "opcode": "value of [VARIABLE]",
                                        "options": {"VARIABLE": "operation"},
                                    },
                                    "text": ""
                                },
                                "OPERAND2": {
                                    "mode": "block-and-text",
                                    "block": None,
                                    "text": "+"
                                }
                            },
                            "options": {}
                        }
                    },
                    "THEN": {
                        "mode": "script",
                        "blocks": [
                            {
                                "opcode": "set [VARIABLE] to (VALUE)",
                                "inputs": {
                                    "VALUE": {
                                        "mode": "block-only",
                                        "block": {
                                            "opcode": "(OPERAND1) + (OPERAND2)",
                                            "inputs": {
                                                "NUM1": {
                                                    "mode": "block-and-text",
                                                    "block": {"opcode": "value of [VARIABLE]", "options": {"VARIABLE": "firstNumber"}},
                                                    "option": ""
                                                },
                                                "NUM2": {
                                                    "mode": "block-and-text",
                                                    "block": {"opcode": "value of [VARIABLE]", "options": {"VARIABLE": "secondNumber"}},
                                                    "option": ""
                                                }
                                            },
                                            "options": {}
                                        }
                                    }
                                },
                                "options": {
                                    "VARIABLE": "result"
                                }
                            }
                        ]
                    }
                },
                "options": {}
            },
            {
                "opcode": "say (MESSAGE) for (SECONDS) seconds",
                "inputs": {
                    "MESSAGE": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "Result: [result]"
                    },
                    "SECONDS": {
                        "mode": "block-and-text",
                        "block": None,
                        "text": "2"
                    }
                },
                "options": {}
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
