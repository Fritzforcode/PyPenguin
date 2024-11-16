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
                    "CONDITION":{"text": "add"},
                    "BODY": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "options": {"VARIABLE": "[ALU] return value"},
                            "inputs": {
                                "VALUE": {"block": {
                                    "opcode": "(NUM1) + (NUM2)",
                                    "inputs": {
                                        "NUM1": {"block": {
                                            "opcode": "value of [VARIABLE]",
                                            "options": {"VARIABLE": "[ALU] Arg A"},
                                        }},
                                        "NUM2": {"block": {
                                            "opcode": "value of [VARIABLE]",
                                            "options": {"VARIABLE": "[ALU] Arg B"},
                                        }},
                                    },
                                }},
                            },
                        },
                    ]},
                },
            },
            {
                "opcode": "case (CONDITION) {BODY}",
                "inputs": {
                    "CONDITION":{"text": "mul"},
                    "BODY": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "options": {"VARIABLE": "[ALU] return value"},
                            "inputs": {
                                "VALUE": {"block": {
                                    "opcode": "(NUM1) * (NUM2)",
                                    "inputs": {
                                        "NUM1": {"block": {
                                            "opcode": "value of [VARIABLE]",
                                            "options": {"VARIABLE": "[ALU] Arg A"},
                                        }},
                                        "NUM2": {"block": {
                                            "opcode": "value of [VARIABLE]",
                                            "options": {"VARIABLE": "[ALU] Arg B"},
                                        }},
                                    },
                                }},
                            },
                        },
                    ]},
                },
            },
        ]},
    },
}

excecuteAluInstrDef = {
    "position": [500,0],
    "blocks": [
        {
            "opcode": "define ...",
            "options": {
                "noScreenRefresh": True,
                "blockType": "instruction",
                "customOpcode": "execute alu instr (instr) (A) (B) (C)",
            }
        },
        {
            "opcode": "if <CONDITION> then {THEN}",
            "inputs": {
                "CONDITION": {"block": {
                    "opcode": "array (array) contains (value) ?",
                    "inputs": {
                        "array": {"text": '["add", "mul"]'},
                        "value": {"block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "instr"},
                        }},
                    },
                }},
                "THEN": {"blocks":[
                    {
                        "opcode": "set [VARIABLE] to (VALUE)",
                        "inputs": {
                            "VALUE": {"block": {
                                "opcode": "call ...",
                                "inputs": {
                                    "reg": {"block": {
                                        "opcode": "value of text argument [VALUE]",
                                        "options": {"VALUE": "A"},
                                    }},
                                },
                                "options": {"customOpcode": "read register (reg)"},
                            }},
                        },
                        "options": {"VARIABLE": "[ALU] Arg A"},
                    },
                    {
                        "opcode": "set [VARIABLE] to (VALUE)",
                        "inputs": {
                            "VALUE": {"block": {
                                "opcode": "call ...",
                                "inputs": {
                                    "reg": {"block": {
                                        "opcode": "value of text argument [VALUE]",
                                        "options": {"VALUE": "B"},
                                    }},
                                },
                                "options": {"customOpcode": "read register (reg)"},
                            }},
                        },
                        "options": {"VARIABLE": "[ALU] Arg B"},
                    },
                ]},
            },
        },
        instructions,
        {
            "opcode": "if <CONDITION> then {THEN}",
            "inputs": {
                "CONDITION": {"block": {
                    "opcode": "array (array) contains (value) ?",
                    "inputs": {
                        "array": {"text": '["add", "mul"]'},
                        "value": {"block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "instr"},
                        }},
                    },
                }},
                "THEN": {"blocks": [
                    {
                        "opcode": "call ...",
                        "inputs": {
                            "reg": {"block": {
                                "opcode": "value of text argument [VALUE]",
                                "options": {"VALUE": "C"},
                            }},
                            "value": {"block": {
                                "opcode": "value of [VARIABLE]",
                                "options": {"VARIABLE": "[ALU] return value"},
                            }},
                        },
                        "options": {"customOpcode": "set register (reg) to (value)"},
                    },
                ]},
            },
        },
    ],
}