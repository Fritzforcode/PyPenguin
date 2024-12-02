readRegisterDef = {
    "position": [1000,0],
    "blocks": [
        {
            "opcode": "define custom block",
            "options": {
                "noScreenRefresh": True,
                "blockType": "numberReporter",
                "customOpcode": "read register (reg)",
            },
        },
        {
            "opcode": "if <CONDITION> then {THEN} else {ELSE}",
            "inputs": {
                "CONDITION": {"block": {
                    "opcode": "(OPERAND1) = (OPERAND2)",
                    "inputs": {
                        "OPERAND1": {"block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "reg"},
                        }},
                        "OPERAND2": {"text": "0"},
                    },
                }},
                "THEN": {"blocks": [
                    {
                        "opcode": "return (return)",
                        "inputs": {
                            "return": {"text": "0"},
                        },
                    },
                ]},
                "ELSE": {"blocks": [
                    {
                        "opcode": "return (return)",
                        "inputs": {
                            "return": {"block": {
                                "opcode": "item (INDEX) of [LIST]",
                                "options": {"LIST": "REGISTERS"},
                                "inputs": {
                                    "INDEX": {"block": {
                                        "opcode": "value of text argument [VALUE]",
                                        "options": {"VALUE": "reg"},
                                    }},
                                },
                            }},
                        },
                    },
                ]},
            },
        },
    ],
}

setRegisterDef = {
    "position": [1500,0],
    "blocks": [
        {
            "opcode": "define custom block",
            "options": {
                "noScreenRefresh": True,
                "blockType": "instruction",
                "customOpcode": "set register (reg) to (value)",
            }, 
        },
        {
            "opcode": "replace item (INDEX) of [LIST] with (ITEM)",
            "inputs": {
                "INDEX": {"block": {
                    "opcode": "value of text argument [VALUE]",
                    "options": {"VALUE": "reg"},
                }},
                "ITEM": {"block": {
                    "opcode": "(NUM1) mod (NUM2)",
                    "inputs": {
                        "NUM1": {"block": {
                            "opcode": "value of text argument [VALUE]",
                            "options": {"VALUE": "value"},
                        }},
                        "NUM2": {"text": "256"},
                    },
                }},
            },
            "options": {"LIST": "REGISTERS"},
        },
    ],
}
