import json
executeCurrentInstrDef = {
    "position": [-1500,0],
    "blocks": [
        {
            "opcode": "define ...",
            "options": {
                "noScreenRefresh": True,
                "blockType": "instruction",
                "customOpcode": "execute current instr",
            }, 
        },
        {
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {
                "VALUE": {"block": {
                    "opcode": "item (INDEX) of [LIST]",
                    "inputs": {
                        "INDEX": {"block": {
                            "opcode": "value of [VARIABLE]",
                            "options": {"VARIABLE": "PROGRAMM COUNTER"},
                        }},
                    },
                    "options": {"LIST": "PROGRAMM"},
                }},
            },
            "options": {"VARIABLE": "current instr"},
        },
        {
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {
                "VALUE": {"block": {
                    "opcode": "(NUM1) + (NUM2)",
                    "inputs": {
                        "NUM1": {"block": {
                            "opcode": "value of [VARIABLE]",
                            "options": {"VARIABLE": "PROGRAMM COUNTER"},
                        }},
                        "NUM2": {"text": "1"},
                    },
                }},
            },
            "options": {"VARIABLE": "NEW PC"},
        },
        {
            "opcode": "if <CONDITION> then {THEN} else {ELSE}",
            "inputs": {
                "CONDITION": {"block": {
                    "opcode": "array (array) contains (value) ?",
                    "inputs": {
                        "array": {"text": '["add", "mul", "addi"]'},
                        "value": {"block": {
                            "opcode": "in array (array) get (index)",
                            "inputs": {
                                "array": {"block": {
                                    "opcode": "value of [VARIABLE]",
                                    "options": {"VARIABLE": "current instr"},
                                }},
                                "index": {"text": "0"},
                            },
                        }},
                    },
                }},
                "THEN": {"blocks": [
                    {
                        "opcode": "call ...",
                        "options": {"customOpcode": "execute alu instr (instr) (A) (B) (C)"},
                        "inputs": {
                            "instr": {"block": {
                                "opcode": "in array (array) get (index)",
                                "inputs": {
                                    "array": {"block": {
                                        "opcode": "value of [VARIABLE]",
                                        "options": {"VARIABLE": "current instr"},
                                    }},
                                    "index": {"text": "0"},
                                },
                            }},
                            "A": {"block": {
                                "opcode": "in array (array) get (index)",
                                "inputs": {
                                    "array": {"block": {
                                        "opcode": "value of [VARIABLE]",
                                        "options": {"VARIABLE": "current instr"},
                                    }},
                                    "index": {"text": "1"},
                                },
                            }},
                            "B": {"block": {
                                "opcode": "in array (array) get (index)",
                                "inputs": {
                                    "array": {"block": {
                                        "opcode": "value of [VARIABLE]",
                                        "options": {"VARIABLE": "current instr"},
                                    }},
                                    "index": {"text": "2"},
                                },
                            }},
                            "C": {"block": {
                                "opcode": "in array (array) get (index)",
                                "inputs": {
                                    "array": {"block": {
                                        "opcode": "value of [VARIABLE]",
                                        "options": {"VARIABLE": "current instr"},
                                    }},
                                    "index": {"text": "3"},
                                },
                            }},
                        },
                    },
                ]},
                "ELSE": {"blocks": [
                    {
                        "opcode": "if <CONDITION> then {THEN} else {ELSE}",
                        "inputs": {
                            "CONDITION": {"block": {
                                "opcode": "array (array) contains (value) ?",
                                "inputs": {
                                    "array": {"text": '["j"]'},
                                    "value": {"block": {
                                        "opcode": "in array (array) get (index)",
                                        "inputs": {
                                            "array": {"block": {
                                                "opcode": "value of [VARIABLE]",
                                                "options": {"VARIABLE": "current instr"},
                                            }},
                                            "index": {"text": "0"},
                                        },
                                    }},
                                },
                            }},
                            "THEN": {"blocks": [
                                {
                                    "opcode": "call ...",
                                    "options": {"customOpcode": "execute control instr (instr) (A) (B) (C)"},
                                    "inputs": {
                                        "instr": {"block": {
                                            "opcode": "in array (array) get (index)",
                                            "inputs": {
                                                "array": {"block": {
                                                    "opcode": "value of [VARIABLE]",
                                                    "options": {"VARIABLE": "current instr"},
                                                }},
                                                "index": {"text": "0"},
                                            },
                                        }},
                                        "A": {"block": {
                                            "opcode": "in array (array) get (index)",
                                            "inputs": {
                                                "array": {"block": {
                                                    "opcode": "value of [VARIABLE]",
                                                    "options": {"VARIABLE": "current instr"},
                                                }},
                                                "index": {"text": "1"},
                                            },
                                        }},
                                        "B": {"block": {
                                            "opcode": "in array (array) get (index)",
                                            "inputs": {
                                                "array": {"block": {
                                                    "opcode": "value of [VARIABLE]",
                                                    "options": {"VARIABLE": "current instr"},
                                                }},
                                                "index": {"text": "2"},
                                            },
                                        }},
                                        "C": {"block": {
                                            "opcode": "in array (array) get (index)",
                                            "inputs": {
                                                "array": {"block": {
                                                    "opcode": "value of [VARIABLE]",
                                                    "options": {"VARIABLE": "current instr"},
                                                }},
                                                "index": {"text": "3"},
                                            },
                                        }},
                                    },
                                },
                            ]},
                            "ELSE": {"blocks": [
                                {
                                    "opcode": "if <CONDITION> then {THEN} else {ELSE}",
                                    "inputs": {
                                        "CONDITION": {"block": {
                                            "opcode": "(OPERAND1) = (OPERAND2)",
                                            "inputs": {
                                                "OPERAND1": {"block": {
                                                    "opcode": "in array (array) get (index)",
                                                    "inputs": {
                                                        "array": {"block": {
                                                            "opcode": "value of [VARIABLE]",
                                                            "options": {"VARIABLE": "current instr"},
                                                        }},
                                                        "index": {"text": "0"},
                                                    },
                                                }},
                                                "OPERAND2": {"text": "hlt"},
                                            },
                                        }},
                                        "THEN": {"blocks": [
                                            {
                                                "opcode": "call ...",
                                                "options": {"customOpcode": "execute control instr (instr) (A) (B) (C)"},
                                                "inputs": {
                                                    "instr": {"block": {
                                                        "opcode": "in array (array) get (index)",
                                                        "inputs": {
                                                            "array": {"block": {
                                                                "opcode": "value of [VARIABLE]",
                                                                "options": {"VARIABLE": "current instr"},
                                                            }},
                                                            "index": {"text": "0"},
                                                        },
                                                    }},
                                                    "A": {"block": {
                                                        "opcode": "in array (array) get (index)",
                                                        "inputs": {
                                                            "array": {"block": {
                                                                "opcode": "value of [VARIABLE]",
                                                                "options": {"VARIABLE": "current instr"},
                                                            }},
                                                            "index": {"text": "1"},
                                                        },
                                                    }},
                                                    "B": {"block": {
                                                        "opcode": "in array (array) get (index)",
                                                        "inputs": {
                                                            "array": {"block": {
                                                                "opcode": "value of [VARIABLE]",
                                                                "options": {"VARIABLE": "current instr"},
                                                            }},
                                                            "index": {"text": "2"},
                                                        },
                                                    }},
                                                    "C": {"block": {
                                                        "opcode": "in array (array) get (index)",
                                                        "inputs": {
                                                            "array": {"block": {
                                                                "opcode": "value of [VARIABLE]",
                                                                "options": {"VARIABLE": "current instr"},
                                                            }},
                                                            "index": {"text": "3"},
                                                        },
                                                    }},
                                                },
                                            },
                                        ]},
                                        "ELSE": {},
                                    },
                                }
                            ]},
                        },
                    },
                ]},
            },
        },
        {
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {
                "VALUE": {"block": {
                    "opcode": "value of [VARIABLE]",
                    "options": {"VARIABLE": "NEW PC"},
                }},
            },
            "options": {"VARIABLE": "PROGRAMM COUNTER"},
        },
    ],
}
programm = [json.dumps(item) for item in [
    ["addi", "0", "1", "1"],
    ["add", "0", "1", "2"],
    ["add", "1", "2", "3"],
    ["add", "2", "3", "4"],
    ["add", "3", "4", "5"],
    ["add", "4", "5", "6"],
    ["add", "5", "6", "7"],
    ["hlt"]
]]

instructions = {
    "opcode": "switch (CONDITION) {CASES}",
    "inputs": {
        "CONDITION": {"block": {
            "opcode": "value of text argument [VALUE]",
            "options": {"VALUE": "instr"},
        }},
        "CASES": {"blocks": [
            {
                "opcode": "case (CONDITION) {BODY}",
                "inputs": {
                    "CONDITION":{"text": "j"},
                    "BODY": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {"block": {
                                    "opcode": "true"
                                }},
                            },
                            "options": {"VARIABLE": "[CRTL] condition met?"},
                        }
                    ]},
                },
            },
        ]},
    },
}

executeControlInstrDef = {
    "position": [-200,0],
    "blocks": [
        {
            "opcode": "define ...",
            "options": {
                "noScreenRefresh": True,
                "blockType": "instruction",
                "customOpcode": "execute control instr (instr) (A) (B) (C)",
            }, 
        },
        instructions,
        {
            "opcode": "if <CONDITION> then {THEN}",
            "inputs": {
                "CONDITION": {"block": {
                    "opcode": "(VALUE) as a boolean",
                    "inputs": {
                        "VALUE": {"block": {
                            "opcode": "value of [VARIABLE]",
                            "options": {"VARIABLE": "[CRTL] condition met?"},
                        }},
                    },
                }},
                "THEN": {"blocks": [
                    {
                        "opcode": "set [VARIABLE] to (VALUE)",
                        "inputs": {
                            "VALUE": {"block": {
                                "opcode": "value of text argument [VALUE]",
                                "options":  {"VALUE": "C"},
                            }},
                        },
                        "options": {"VARIABLE": "NEW PC"},
                    },
                ]},
            },
        },
    ],
}
