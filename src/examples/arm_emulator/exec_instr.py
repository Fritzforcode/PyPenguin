from helpers import varReporterBlock

setArgs = [
    {
        "opcode": "set [VARIABLE] to (VALUE)",
        "inputs": {
            "VALUE": {"block": {
                "opcode": "call custom block",
                "inputs": {
                    "key": {"text": id},
                    "json": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "instr"]},
                    }},
                    "default": {"text": "null"},
                },
                "options": {"customOpcode": ["value", "get (key) from (json) else (default)"]},
            }},
        },
        "options": {"VARIABLE": ["variable", id]},
    } for id in ["arg0", "arg1", "arg2"]
]

moveCase = {
    "opcode": "case (CONDITION) {BODY}",
    "inputs": {
        "CONDITION": {"text": "move"},
        "BODY": {"blocks": [
            {
                "opcode": "switch (CONDITION) {CASES}",
                "inputs": {
                    "CONDITION": {"block": varReporterBlock("instr")},
                    "CASES": {"blocks": [
                        {
                            "opcode": "case (CONDITION) {BODY}",
                            "inputs": {
                                "CONDITION": {"text": "mov"},
                                "BODY": {"blocks": [
                                    {
                                        "opcode": "call custom block",
                                        "inputs": {
                                            "register": {"block": varReporterBlock("arg0")},
                                            "value"   : {"block": varReporterBlock("arg1")},
                                        },
                                        "options": {"customOpcode": ["value", "set register (register) to (value)"]},
                                    },
                                ]}
                            },
                        },
                        {
                            "opcode": "case (CONDITION) {BODY}",
                            "inputs": {
                                "CONDITION": {"text": "mvn"},
                                "BODY": {"blocks": [
                                    {
                                        "opcode": "call custom block",
                                        "inputs": {
                                            "register": {"block": varReporterBlock("arg0")},
                                            "value": {"block": {
                                                "opcode": "not (NUM)",
                                                "inputs": {
                                                    "NUM": {"block": varReporterBlock("arg1")},
                                                },
                                            }},
                                        },
                                        "options": {"customOpcode": ["value", "set register (register) to (value)"]},
                                    },
                                ]}
                            },
                        },
                    ]},
                },
            },
        ]},
    },
}

aluSubcases = []
for opcode, instr in [
    ("(OPERAND1) + (OPERAND2)", "add"),
    ("(OPERAND1) - (OPERAND2)", "sub"),
    ("(OPERAND1) * (OPERAND2)", "mul"),
    ("(OPERAND1) / (OPERAND2)", "div"),
    ("(OPERAND1) and (OPERAND2)", "and"),
    ("(OPERAND1) or (OPERAND2)", "orr"),
    ("(OPERAND1) xor (OPERAND2)", "eor"),
    ("(NUM) << (BITS)", "lsl"),
    ("(NUM) >> (BITS)", "lsr"),
]:
    if instr in ["lsl", "lsr"]:
        id1, id2 = "NUM", "BITS"
    else:
        id1, id2 = "OPERAND1", "OPERAND2"   
    if instr == "div":
        aluSubcases.append({
        "opcode": "case (CONDITION) {BODY}",
        "inputs": {
            "CONDITION": {"text": instr},
            "BODY": {"blocks": [
                {
                    "opcode": "set [VARIABLE] to (VALUE)",
                    "inputs": {
                        "VALUE": {"block": {
                            "opcode": "if <CONDITION> then (TRUEVALUE) else (FALSEVALUE)",
                            "inputs": {
                                "CONDITION": {"block": {
                                    "opcode": "(OPERAND1) = (OPERAND2)",
                                    "inputs": {
                                        "OPERAND1": {"block": varReporterBlock("value2")},
                                        "OPERAND2": {"text": "0"},
                                    },
                                }},
                                "TRUEVALUE": {"text": "0"},
                                "FALSEVALUE": {"block": {
                                    "opcode": "[OPERATION] of (NUM)",
                                    "inputs": {
                                        "NUM": {"block": {
                                            "opcode": opcode,
                                            "inputs": {
                                                id1: {"block": varReporterBlock("value1")},
                                                id2: {"block": varReporterBlock("value2")},
                                            },
                                        }},
                                    },
                                    "options": {"OPERATION": ["value", "floor"]},
                                }},
                            },
                        }},
                    },
                    "options": {"VARIABLE": ["variable", "result"]},
                },
            ]},
        },
    })
    else:
        aluSubcases.append({
        "opcode": "case (CONDITION) {BODY}",
        "inputs": {
            "CONDITION": {"text": instr},
            "BODY": {"blocks": [
                {
                    "opcode": "set [VARIABLE] to (VALUE)",
                    "inputs": {
                        "VALUE": {"block": {
                            "opcode": opcode,
                            "inputs": {
                                id1: {"block": varReporterBlock("value1")},
                                id2: {"block": varReporterBlock("value2")},
                            },
                        }},
                    },
                    "options": {"VARIABLE": ["variable", "result"]},
                },
            ]},
        },
    })

aluCase = {
    "opcode": "case (CONDITION) {BODY}",
    "inputs": {
        "CONDITION": {"text": "alu"},
        "BODY": {"blocks": [
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {"block": {
                        "opcode": "call custom block",
                        "inputs": {
                            "register": {"block": varReporterBlock("arg1")},
                        },
                        "options": {"customOpcode": ["value", "get register (register)"]},
                    }},
                },
                "options": {"VARIABLE": ["variable", "value1"]},
            },
            {
                "opcode": "if <CONDITION> then {THEN} else {ELSE}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "(STRING) is number?",
                        "inputs": {
                            "STRING": {"block": varReporterBlock("arg2")},
                        },
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {"block": varReporterBlock("arg2")},
                            },
                            "options": {"VARIABLE": ["variable", "value2"]},
                        },
                    ]},
                    "ELSE": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {"block": {
                                    "opcode": "call custom block",
                                    "inputs": {
                                        "register": {"block": varReporterBlock("arg2")},
                                    },
                                    "options": {"customOpcode": ["value", "get register (register)"]},
                                }},
                            },
                            "options": {"VARIABLE": ["variable", "value2"]},
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "(OPERAND1) = (OPERAND2)",
                        "inputs": {
                            "OPERAND1": {"block": varReporterBlock("instr")},
                            "OPERAND2": {"text": "addi"},
                        },
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {"VALUE": {"text": "add"}},
                            "options": {"VARIABLE": ["variable", "instr"]},
                        },
                    ]},
                },
            },
            {
                "opcode": "switch (CONDITION) {CASES}",
                "inputs": {
                    "CONDITION": {"block": varReporterBlock("instr")},
                    "CASES": {"blocks": aluSubcases},
                },
            },
            {
                "opcode": "call custom block",
                "inputs": {
                    "register": {"block": varReporterBlock("arg0")},
                    "value": {"block": varReporterBlock("result")},
                },
                "options": {"customOpcode": ["value", "set register (register) to (value)"]},
            },
        ]},
    },
}

memoryCase = {
    "opcode": "case (CONDITION) {BODY}",
    "inputs": {
        "CONDITION": {"text": "memory"},
        "BODY": {"blocks": [
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {"block": {
                        "opcode": "call custom block",
                        "inputs": {
                            "register": {"block": varReporterBlock("arg1")},
                        },
                        "options": {"customOpcode": ["value", "get register (register)"]},
                    }},
                },
                "options": {"VARIABLE": ["variable", "address"]},
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "(OPERAND1) != (OPERAND2)",
                        "inputs": {
                            "OPERAND1": {"block": varReporterBlock("arg2")},
                            "OPERAND2": {"text": "null"},
                        },
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "change [VARIABLE] by (VALUE)",
                            "inputs": {
                                "VALUE": {"block": varReporterBlock("arg2")},
                            },
                            "options": {"VARIABLE": ["variable", "address"]},
                        },
                    ]},
                },
            },
            {
                "opcode": "switch (CONDITION) {CASES}",
                "inputs": {
                    "CONDITION": {"block": varReporterBlock("instr")},
                    "CASES": {"blocks": [
                        {
                            "opcode": "case (CONDITION) {BODY}",
                            "inputs": {
                                "CONDITION": {"text": "ldr"},
                                "BODY": {"blocks": [
                                    {
                                        "opcode": "call custom block",
                                        "inputs": {
                                            "register": {"block": varReporterBlock("arg0")},
                                            "value": {"block": {
                                                "opcode": "call custom block",
                                                "inputs": {
                                                    "address": {"block": varReporterBlock("address")},
                                                },
                                                "options": {"customOpcode": ["value", "get memory (address)"]},
                                            }},
                                        },
                                        "options": {"customOpcode": ["value", "set register (register) to (value)"]},
                                    },
                                ]},
                            },
                        },
                        {
                            "opcode": "case (CONDITION) {BODY}",
                            "inputs": {
                                "CONDITION": {"text": "str"},
                                "BODY": {"blocks": [
                                    {
                                        "opcode": "call custom block",
                                        "inputs": {
                                            "address": {"block": varReporterBlock("address")},
                                            "value": {"block": {
                                                "opcode": "call custom block",
                                                "inputs": {
                                                    "register": {"block": varReporterBlock("arg0")},
                                                },
                                                "options": {"customOpcode": ["value", "get register (register)"]},
                                            }},
                                        },
                                        "options": {"customOpcode": ["value", "set memory (address) to (value)"]},
                                    },
                                ]},
                            },
                        }
                    ]},
                },
            },
        ]},
    },
}

setFlags = {
    "opcode": "set [VARIABLE] to (VALUE)",
    "inputs": {
        "VALUE": {"block": {
            "opcode": "set (KEY) to (VALUE) in (JSON)",
            "inputs": {
                "KEY": {"text": "zero"},
                "VALUE": {"block": {
                    "opcode": "(OPERAND1) = (OPERAND2)",
                    "inputs": {
                        "OPERAND1": {"block": varReporterBlock("result")},
                        "OPERAND2": {"text": "0"},
                    },
                }},
                "JSON": {"block": {
                    "opcode": "set (KEY) to (VALUE) in (JSON)",
                    "inputs": {
                        "KEY": {"text": "negative"},
                        "VALUE": {"block": {
                            "opcode": "(OPERAND1) < (OPERAND2)",
                            "inputs": {
                                "OPERAND1": {"block": varReporterBlock("result")},
                                "OPERAND2": {"text": "0"},
                            },
                        }},
                        "JSON": {"text": "{}"}
                    },
                }},
            },
        }},
    },
    "options": {"VARIABLE": ["variable", "flags"]},
}

comparisonCase = {
    "opcode": "case (CONDITION) {BODY}",
    "inputs": {
        "CONDITION": {"text": "comparison"},
        "BODY": {"blocks": [
            {
                "opcode": "switch (CONDITION) {CASES}",
                "inputs": {
                    "CONDITION": {"block": varReporterBlock("instr")},
                    "CASES": {"blocks": [
                        {
                            "opcode": "case (CONDITION) {BODY}",
                            "inputs": {
                                "CONDITION": {"text": "cmp"},
                                "BODY": {"blocks": [
                                    {
                                        "opcode": "set [VARIABLE] to (VALUE)",
                                        "inputs": {
                                            "VALUE": {"block": {
                                                "opcode": "(OPERAND1) - (OPERAND2)",
                                                "inputs": {
                                                    "OPERAND1": {"block": {
                                                        "opcode": "call custom block",
                                                        "inputs": {
                                                            "register": {"block": varReporterBlock("arg0")},
                                                        },
                                                        "options": {"customOpcode": ["value", "get register (register)"]},
                                                    }},
                                                    "OPERAND2": {"block": varReporterBlock("arg1")},
                                                },
                                            }},
                                        },
                                        "options": {"VARIABLE": ["variable", "result"]},
                                    },
                                    setFlags,
                                ]},
                            },
                        },
                    ]},
                },
            },
        ]}
    },
}

branchCase = {
    "opcode": "case (CONDITION) {BODY}",
    "inputs": {
        "CONDITION": {"text": "branch"},
        "BODY": {"blocks": [
            {
                "opcode": "switch (CONDITION) {CASES}",
                "inputs": {
                    "CONDITION": {"block": varReporterBlock("instr")},
                    "CASES": {"blocks": [
                        {
                            "opcode": "case (CONDITION) {BODY}",
                            "inputs": {
                                "CONDITION": {"text": "bge"},
                                "BODY": {"blocks": [
                                    {
                                        "opcode": "set [VARIABLE] to (VALUE)",
                                        "inputs": {
                                            "VALUE": {"block": {
                                                "opcode": "not <OPERAND>",
                                                "inputs": {
                                                    "OPERAND": {"block": {
                                                        "opcode": "(VALUE) as a boolean",
                                                        "inputs": {
                                                            "VALUE": {"block": {
                                                                "opcode": "get (KEY) from (JSON)",
                                                                "inputs": {
                                                                    "KEY": {"text": "negative"},
                                                                    "JSON": {"block": varReporterBlock("flags")},
                                                                },
                                                            }}
                                                        },
                                                    }},
                                                },
                                            }},
                                        },
                                        "options": {"VARIABLE": ["variable", "do branch"]},
                                    },
                                    {
                                        "opcode": "set [VARIABLE] to (VALUE)",
                                        "inputs": {
                                            "VALUE": {"block": varReporterBlock("arg0")},
                                        },
                                        "options": {"VARIABLE": ["variable", "target pc"]},
                                    },
                                ]},
                            },
                        },
                    ]},
                },
            },
            {
                "opcode": "if <CONDITION> then {THEN}",
                "inputs": {
                    "CONDITION": {"block": {
                        "opcode": "(VALUE) as a boolean",
                        "inputs": {
                            "VALUE": {"block": varReporterBlock("do branch")},
                        },
                    }},
                    "THEN": {"blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {"block": varReporterBlock("target pc")},
                            },
                            "options": {"VARIABLE": ["variable", "program counter"]},
                        },
                        {
                            "opcode": "return (VALUE)",
                            "inputs": {
                                "VALUE": {"text": ""},
                            },
                        },
                    ]},
                },
            },
        ]},
    },
}

executeInstr = {"position": [0,0], "blocks": [
    {
        "opcode": "define custom block",
        "options": {"noScreenRefresh": ["value", True], "blockType": ["value", "instruction"], "customOpcode": ["value", "execute instr (instr)"]},
    },
    {
        "opcode": "set [VARIABLE] to (VALUE)",
        "inputs": {
            "VALUE": {"block": {
                "opcode": "get (KEY) from (JSON)",
                "inputs": {
                    "KEY": {"text": "type"},
                    "JSON": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "instr"]},
                    }},
                },
            }},
        },
        "options": {"VARIABLE": ["variable", "instr type"]},
    },
    {
        "opcode": "set [VARIABLE] to (VALUE)",
        "inputs": {
            "VALUE": {"block": {
                "opcode": "get (KEY) from (JSON)",
                "inputs": {
                    "KEY": {"text": "instr"},
                    "JSON": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "instr"]},
                    }},
                },
            }},
        },
        "options": {"VARIABLE": ["variable", "instr"]},
    },
    *setArgs,
    {
        "opcode": "switch (CONDITION) {CASES}",
        "inputs": {
            "CONDITION": {"block": varReporterBlock("instr type")},
            "CASES": {"blocks": [
                moveCase,
                aluCase,
                memoryCase,
                comparisonCase,
                branchCase,
            ]},
        },
    },
    {
        "opcode": "change [VARIABLE] by (VALUE)",
        "inputs": {
            "VALUE": {"text": "1"},
        },
        "options": {"VARIABLE": ["variable", "program counter"]},
    },
]}
