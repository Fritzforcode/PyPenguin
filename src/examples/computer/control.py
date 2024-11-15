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
            "opcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
            "inputs": {
                "CONDITION": {"block": {
                    "opcode": "array (array) contains (value) ?",
                    "inputs": {
                        "array": {"text": '["add", "mul"]'},
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
                "SUBSTACK": {"blocks": [
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
                "SUBSTACK2": {"blocks": [
                    {
                        "opcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
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
                            "SUBSTACK": {"blocks": [
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
                            "SUBSTACK2": {},
                        },
                    },
                ]},
            },
        },
    ],
}
programm = [json.dumps(item) for item in [
    ["add", "1", "0", "2"],
    ["add", "1", "2", "3"],
    ["add", "2", "3", "4"],
]]

executeControlInstrDef = {
    "position": [0,0],
    "blocks": [
        {
            "opcode": "define ...",
            "options": {
                "noScreenRefresh": True,
                "blockType": "instruction",
                "customOpcode": "execute control instr (instr) (A) (B) (C)",
            }, 
        },
    ],
}
