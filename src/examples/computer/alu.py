add = {
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
}

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
                        add,
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
            {
                "opcode": "case (CONDITION) {BODY}",
                "inputs": {
                    "CONDITION":{"text": "addi"},
                    "BODY": {"blocks": [
                        add,
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
            "opcode": "if <CONDITION> then {THEN} else {ELSE}",
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
                                        "options": {"VALUE": "B"},
                                    }},
                                },
                                "options": {"customOpcode": "read register (reg)"},
                            }},
                        },
                        "options": {"VARIABLE": "[ALU] Arg B"},
                    },
                ]},
                "ELSE": {"blocks": [
                    {
                        "opcode": "set [VARIABLE] to (VALUE)",
                        "inputs": {
                            "VALUE": {"block": {
                                "opcode": "value of text argument [VALUE]",
                                "options": {"VALUE": "B"},
                            }},
                        },
                        "options": {"VARIABLE": "[ALU] Arg B"},
                    },
                ]},
            },
        },
        instructions,
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
    ],
}