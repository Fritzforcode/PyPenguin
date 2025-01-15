touchingPaddleBlock = {
    "opcode": "<OPERAND1> or <OPERAND2>",
    "inputs": {
        "OPERAND1": {"block": {
            "opcode": "touching ([OBJECT]) ?",
            "inputs": {
                "OBJECT": {"option": "Paddle 1"},
            },
        }},
        "OPERAND2": {"block": {
            "opcode": "touching ([OBJECT]) ?",
            "inputs": {
                "OBJECT": {"option": "Paddle 2"},
            },
        }},
    },
}

overYLimitBlock = {
    "opcode": "<OPERAND1> or <OPERAND2>",
    "inputs": {
        "OPERAND1": {"block": {
            "opcode": "(OPERAND1) > (OPERAND2)",
            "inputs": {
                "OPERAND1": {"block": {
                    "opcode": "y position",
                }},
                "OPERAND2": {"text": "156"},
            },
        }},
        "OPERAND2": {"block": {
            "opcode": "(OPERAND1) < (OPERAND2)",
            "inputs": {
                "OPERAND1": {"block": {
                    "opcode": "y position",
                }},
                "OPERAND2": {"text": "-156"},
            },
        }},
    },
}

ballCode = {"position": [0, 0], "blocks": [
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
                "opcode": "pick random (OPERAND1) to (OPERAND2)",
                "inputs": {
                    "OPERAND1": {"text": "45"},
                    "OPERAND2": {"text": "135"},
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
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": touchingPaddleBlock},
                    "THEN": {"blocks": [
                        {
                            "opcode": "point in direction (DIRECTION)",
                            "inputs": {
                                "DIRECTION": {"block": {
                                    "opcode": "(OPERAND1) - (OPERAND2)",
                                    "inputs": {
                                        "OPERAND1": {"text": ""},
                                        "OPERAND2": {"block": {
                                            "opcode": "direction"
                                        }},
                                    },
                                }},
                            },
                        },
                        {
                            "opcode": "change [VARIABLE] by (VALUE)",
                            "inputs": {"VALUE": {"text": "1"}},
                            "options": {"VARIABLE": "Speed"},
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": overYLimitBlock},
                    "THEN": {"blocks": [
                        {
                            "opcode": "point in direction (DIRECTION)",
                            "inputs": {
                                "DIRECTION": {"block": {
                                    "opcode": "(OPERAND1) - (OPERAND2)",
                                    "inputs": {
                                        "OPERAND1": {"text": "180"},
                                        "OPERAND2": {"block": {
                                            "opcode": "direction"
                                        }},
                                    },
                                }},
                            },
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "(OPERAND1) > (OPERAND2)",
                        "inputs": {
                            "OPERAND1": {"block": {
                                "opcode": "x position"
                            }},
                            "OPERAND2": {"text": "216"},
                        },
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "broadcast ([MESSAGE])",
                            "inputs": {
                                "MESSAGE": {"option": "Player 1 Scores"},
                            },
                        },
                        {
                            "opcode": "stop script [TARGET]",
                            "options": {"TARGET": "this script"},
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "(OPERAND1) < (OPERAND2)",
                        "inputs": {
                            "OPERAND1": {"block": {
                                "opcode": "x position"
                            }},
                            "OPERAND2": {"text": "-216"},
                        },
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "broadcast ([MESSAGE])",
                            "inputs": {
                                "MESSAGE": {"option": "Player 2 Scores"},
                            },
                        },
                        {
                            "opcode": "stop script [TARGET]",
                            "options": {"TARGET": "this script"},
                        },
                    ]},
                },
            },
        ]}},
    },
]}

paddleOneCode = {"position": [0, 0], "blocks": [
    {
        "opcode": "when green flag clicked"
    },
    {
        "opcode": "go to x: (X) y: (Y)",
        "inputs": {
            "X": {"text": "-220"},
            "Y": {"text": "0"},
        },
    },
    {
        "opcode": "forever {BODY}",
        "inputs": {"BODY": {"blocks": [
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "key ([KEY]) pressed?",
                        "inputs": {"KEY": {"option": "w"}},
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "change y by (DY)",
                            "inputs": {
                                "DY": {"text": "10"},
                            },
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "key ([KEY]) pressed?",
                        "inputs": {"KEY": {"option": "s"}},
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "change y by (DY)",
                            "inputs": {
                                "DY": {"text": "-10"},
                            },
                        },
                    ]},
                },
            },
        ]}},
    },
]}

paddleTwoCode = {"position": [0, 0], "blocks": [
    {
        "opcode": "when green flag clicked"
    },
    {
        "opcode": "go to x: (X) y: (Y)",
        "inputs": {
            "X": {"text": "220"},
            "Y": {"text": "0"},
        },
    },
    {
        "opcode": "forever {BODY}",
        "inputs": {"BODY": {"blocks": [
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "key ([KEY]) pressed?",
                        "inputs": {"KEY": {"option": "up arrow"}},
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "change y by (DY)",
                            "inputs": {
                                "DY": {"text": "10"},
                            },
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "key ([KEY]) pressed?",
                        "inputs": {"KEY": {"option": "down arrow"}},
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "change y by (DY)",
                            "inputs": {
                                "DY": {"text": "-10"},
                            },
                        },
                    ]},
                },
            },
        ]}},
    },
]}

whenPlayerOneScores = {"position": [0, 0], "blocks": [
    {
        "opcode": "when I receive [MESSAGE]",
        "options": {"MESSAGE": "Player 1 Scores"},
    },
    {
        "opcode": "change [VARIABLE] by (VALUE)",
        "inputs": {
            "VALUE": {"text": "1"},
        },
        "options": {"VARIABLE": "Player 1 Score"},
    },
    {
        "opcode": "broadcast ([MESSAGE])",
        "inputs": {"MESSAGE": {"option": "Reset Ball"}},
    },
    {
        "opcode": "run flag",
    },
]}

whenPlayerTwoScores = {"position": [0, 300], "blocks": [
    {
        "opcode": "when I receive [MESSAGE]",
        "options": {"MESSAGE": "Player 2 Scores"},
    },
    {
        "opcode": "change [VARIABLE] by (VALUE)",
        "inputs": {
            "VALUE": {"text": "1"},
        },
        "options": {"VARIABLE": "Player 2 Score"},
    },
    {
        "opcode": "run flag",
    },
]}

# ['instruction', 'lastInstruction', 'textReporter', 'OPERANDberReporter', 'booleanReporter']
projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [whenPlayerOneScores, whenPlayerTwoScores],
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
            "costumes": [
                {
                    "name": "Basketball",
                    "extension": "svg",
                    "bitmapResolution": 1,
                    "rotationCenter": [23, 23],
                }
            ],
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
            "rotationStyle": "left-right",
        },
        {
            "name": "Paddle 1",
            "isStage": False,
            "scripts": [paddleOneCode],
            "comments": [],
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "rectangle",
                    "extension": "svg",
                    "bitmapResolution": 1,
                    "rotationCenter": [9.083, 67.25],
                },
            ],
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
            "name": "Paddle 2",
            "isStage": False,
            "scripts": [paddleTwoCode],
            "comments": [],
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "rectangle",
                    "extension": "svg",
                    "bitmapResolution": 1,
                    "rotationCenter": [9.083, 67.25],
                },
            ],
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
        {
            "name": "Player 1 Score",
            "currentValue": "",
            "isCloudVariable": False,
        },
        {
            "name": "Player 2 Score",
            "currentValue": "",
            "isCloudVariable": False,
        },
    ],
    "globalLists": [],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "monitors": [
        {
            "opcode": "value of [VARIABLE]",
            "options": {"VARIABLE": "Speed"},
            "spriteName": None,
            "position": [10, 10],
            "visible": True,
            "sliderMin": 0,
            "sliderMax": 100,
            "onlyIntegers": True,
        },
        {
            "opcode": "value of [VARIABLE]",
            "options": {"VARIABLE": "Player 1 Score"},
            "spriteName": None,
            "position": [0, 338],
            "visible": True,
            "sliderMin": 0,
            "sliderMax": 100,
            "onlyIntegers": True,
        },
        {
            "opcode": "value of [VARIABLE]",
            "options": {"VARIABLE": "Player 2 Score"},
            "spriteName": None,
            "position": [328, 338],
            "visible": True,
            "sliderMin": 0,
            "sliderMax": 100,
            "onlyIntegers": True,
        },
    ],
    "extensionData": {},
    "extensions": [],
}
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.utility import writeJSONFile, pp

validateProject(projectData=projectData)
#pp(projectData)

writeJSONFile(
    filePath = "temp2.json",
    data     = projectData
)

writeJSONFile(
    filePath = "pong/project.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDir = "pong",
    projectFilePath     = "export.pmp",
    temporaryDir        = "temporary",
    writeDebugFiles     = True,
)
