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

from pypenguin.utility import readJSONFile
projectData = readJSONFile("btt/project.json")

projectData2 = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100
        },
        {
            "name": "Sprite1",
            "isStage": False,
            "scripts": [
                {
                    "position": [
                        0,
                        0
                    ],
                    "blocks": [
                        {
                            "opcode": "define custom block",
                            "inputs": {},
                            "options": {
                                "noScreenRefresh": [
                                    "value",
                                    True
                                ],
                                "customOpcode": [
                                    "value",
                                    "set (var) . (key) to (value)"
                                ],
                                "blockType": [
                                    "value",
                                    "instruction"
                                ]
                            }
                        },
                        {
                            "opcode": "set runtime var (VARIABLE) to (VALUE)",
                            "inputs": {
                                "VARIABLE": {
                                    "block": {
                                        "opcode": "value of text [ARGUMENT]",
                                        "inputs": {},
                                        "options": {
                                            "ARGUMENT": [
                                                "value",
                                                "var"
                                            ]
                                        }
                                    }
                                },
                                "VALUE": {
                                    "block": {
                                        "opcode": "set (KEY) to (VALUE) in (JSON)",
                                        "inputs": {
                                            "KEY": {
                                                "block": {
                                                    "opcode": "value of text [ARGUMENT]",
                                                    "inputs": {},
                                                    "options": {
                                                        "ARGUMENT": [
                                                            "value",
                                                            "key"
                                                        ]
                                                    }
                                                }
                                            },
                                            "VALUE": {
                                                "block": {
                                                    "opcode": "value of text [ARGUMENT]",
                                                    "inputs": {},
                                                    "options": {
                                                        "ARGUMENT": [
                                                            "value",
                                                            "value"
                                                        ]
                                                    }
                                                }
                                            },
                                            "JSON": {
                                                "block": {
                                                    "opcode": "runtime var (VARIABLE)",
                                                    "inputs": {
                                                        "VARIABLE": {
                                                            "block": {
                                                                "opcode": "value of text [ARGUMENT]",
                                                                "inputs": {},
                                                                "options": {
                                                                    "ARGUMENT": [
                                                                        "value",
                                                                        "var"
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "options": {}
                                                }
                                            }
                                        },
                                        "options": {}
                                    }
                                }
                            },
                            "options": {}
                        }
                    ]
                },
                {
                    "position": [
                        1000,
                        0
                    ],
                    "blocks": [
                        {
                            "opcode": "define custom block",
                            "inputs": {},
                            "options": {
                                "noScreenRefresh": [
                                    "value",
                                    True
                                ],
                                "customOpcode": [
                                    "value",
                                    "change (var) . (key) by (value)"
                                ],
                                "blockType": [
                                    "value",
                                    "instruction"
                                ]
                            }
                        },
                        {
                            "opcode": "call custom block",
                            "inputs": {
                                "var": {
                                    "block": {
                                        "opcode": "value of text [ARGUMENT]",
                                        "inputs": {},
                                        "options": {
                                            "ARGUMENT": [
                                                "value",
                                                "var"
                                            ]
                                        }
                                    }
                                },
                                "key": {
                                    "block": {
                                        "opcode": "value of text [ARGUMENT]",
                                        "inputs": {},
                                        "options": {
                                            "ARGUMENT": [
                                                "value",
                                                "key"
                                            ]
                                        }
                                    }
                                },
                                "value": {
                                    "block": {
                                        "opcode": "(OPERAND1) + (OPERAND2)",
                                        "inputs": {
                                            "OPERAND1": {
                                                "block": {
                                                    "opcode": "get (KEY) from (JSON)",
                                                    "inputs": {
                                                        "KEY": {
                                                            "block": {
                                                                "opcode": "value of text [ARGUMENT]",
                                                                "inputs": {},
                                                                "options": {
                                                                    "ARGUMENT": [
                                                                        "value",
                                                                        "key"
                                                                    ]
                                                                }
                                                            }
                                                        },
                                                        "JSON": {
                                                            "block": {
                                                                "opcode": "runtime var (VARIABLE)",
                                                                "inputs": {
                                                                    "VARIABLE": {
                                                                        "block": {
                                                                            "opcode": "value of text [ARGUMENT]",
                                                                            "inputs": {},
                                                                            "options": {
                                                                                "ARGUMENT": [
                                                                                    "value",
                                                                                    "var"
                                                                                ]
                                                                            }
                                                                        }
                                                                    }
                                                                },
                                                                "options": {}
                                                            }
                                                        }
                                                    },
                                                    "options": {}
                                                }
                                            },
                                            "OPERAND2": {
                                                "block": {
                                                    "opcode": "value of text [ARGUMENT]",
                                                    "inputs": {},
                                                    "options": {
                                                        "ARGUMENT": [
                                                            "value",
                                                            "value"
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        "options": {}
                                    }
                                }
                            },
                            "options": {
                                "customOpcode": [
                                    "value",
                                    "set (var) . (key) to (value)"
                                ]
                            }
                        }
                    ]
                }
            ],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "position": [
                0,
                0
            ],
            "size": 100,
            "direction": 90,
            "draggable": True,
            "rotationStyle": "all around",
            "localVariables": [],
            "localLists": []
        }
    ],
    "globalVariables": [
        {
            "name": "ADDRESSING",
            "currentValue": "",
            "isCloudVariable": False
        },
        {
            "name": "OPCODES",
            "currentValue": "",
            "isCloudVariable": False
        },
        {
            "name": "BYTEORDER",
            "currentValue": "",
            "isCloudVariable": False
        },
        {
            "name": "PAGE_WRAPPING_BUG",
            "currentValue": "",
            "isCloudVariable": False
        }
    ],
    "globalLists": [],
    "monitors": [],
    "extensions": [
        "jgJSON",
        "lmsTempVars2",
        "Bitwise"
    ],
    "extensionURLs": {
        "Bitwise": "https://extensions.turbowarp.org/bitwise.js"
    }
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
