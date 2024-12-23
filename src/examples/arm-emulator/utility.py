setRegister = {"position": [1000, 0], "blocks": [
    {
        "opcode": "define custom block",
        "options": {
            "noScreenRefresh": ["value", True],
            "blockType": ["value", "instruction"],
            "customOpcode": ["value", "set register (register) to (value)"]
        },
    },
    {
        "opcode": "replace item (INDEX) of [LIST] with (ITEM)",
        "inputs": {
            "INDEX": {"block": {
                "opcode": "get (KEY) from (JSON)",
                "inputs": {
                    "KEY": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "register"]},
                    }},
                    "JSON": {"block": {
                        "opcode": "value of [VARIABLE]",
                        "options": {"VARIABLE": ["variable", "register map"]},
                    }},
                },
            }},
            "ITEM": {"block": {
                "opcode": "value of text [ARGUMENT]",
                "options": {"ARGUMENT": ["value", "value"]},
            }},
        },
        "options": {"LIST": ["list", "registers"]},
    },
]}

getRegister = {"position": [1000, 250], "blocks": [
    {
        "opcode": "define custom block",
        "options": {
            "noScreenRefresh": ["value", True],
            "blockType": ["value", "textReporter"],
            "customOpcode": ["value", "get register (register)"]
        },
    },
    {
        "opcode": "return (VALUE)",
        "inputs": {
            "VALUE": {"block": {
                "opcode": "item (INDEX) of [LIST]",
                "inputs": {
                    "INDEX": {"block": {
                        "opcode": "get (KEY) from (JSON)",
                        "inputs": {
                            "KEY": {"block": {
                                "opcode": "value of text [ARGUMENT]",
                                "options": {"ARGUMENT": ["value", "register"]},
                            }},
                            "JSON": {"block": {
                                "opcode": "value of [VARIABLE]",
                                "options": {"VARIABLE": ["variable", "register map"]},
                            }},
                        },
                    }},
                },
                "options": {"LIST": ["list", "registers"]},
            }},
        },
    },
]}

setMemory = {"position": [1750, 0], "blocks": [
    {
        "opcode": "define custom block",
        "options": {
            "noScreenRefresh": ["value", True],
            "blockType": ["value", "instruction"],
            "customOpcode": ["value", "set memory (address) to (value)"]
        },
    },
    {
        "opcode": "set [VARIABLE] to (VALUE)",
        "inputs": {
            "VALUE": {"block": {
                "opcode": "set (KEY) to (VALUE) in (JSON)",
                "inputs": {
                    "KEY": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "address"]},
                    }},
                    "VALUE": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "value"]},
                    }},
                    "JSON": {"block": {
                        "opcode": "value of [VARIABLE]",
                        "options": {"VARIABLE": ["variable", "memory"]},
                    }},
                },
            }},
        },
        "options": {"VARIABLE": ["variable", "memory"]},
    },
]}

getMemory = {"position": [1750, 250], "blocks": [
    {
        "opcode": "define custom block",
        "options": {
            "noScreenRefresh": ["value", True],
            "blockType": ["value", "textReporter"],
            "customOpcode": ["value", "get memory (address)"]
        },
    },
    {
        "opcode": "return (VALUE)",
        "inputs": {
            "VALUE": {"block": {
                "opcode": "call custom block",
                "inputs": {
                    "key": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "address"]},
                    }},
                    "json": {"block": {
                        "opcode": "value of [VARIABLE]",
                        "options": {"VARIABLE": ["variable", "memory"]},
                    }},
                    "default": {"text": "0"},
                },
                "options": {"customOpcode": ["value", "get (key) from (json) else (default)"]},
            }},
        },
    },
]}

getKeyElseDefault = {"position": [2500, 0], "blocks": [
    {
        "opcode": "define custom block",
        "options": {
            "noScreenRefresh": ["value", True],
            "blockType": ["value", "textReporter"],
            "customOpcode": ["value", "get (key) from (json) else (default)"]
        },
    },
    {
        "opcode": "if <CONDITION> then {THEN} else {ELSE}",
        "inputs": {
            "CONDITION": {"block": {
                "opcode": "json (JSON) has key (KEY) ?",
                "inputs": {
                    "JSON": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "json"]},
                    }},
                    "KEY": {"block": {
                        "opcode": "value of text [ARGUMENT]",
                        "options": {"ARGUMENT": ["value", "key"]},
                    }},
                },
            }},
            "THEN": {"blocks": [
                {
                    "opcode": "return (VALUE)",
                    "inputs": {
                        "VALUE": {"block": {
                            "opcode": "get (KEY) from (JSON)",
                            "inputs": {
                                "KEY": {"block": {
                                    "opcode": "value of text [ARGUMENT]",
                                    "options": {"ARGUMENT": ["value", "key"]},
                                }},
                                "JSON": {"block": {
                                    "opcode": "value of text [ARGUMENT]",
                                    "options": {"ARGUMENT": ["value", "json"]},
                                }},
                            },
                        }},
                    },
                },
            ]},
            "ELSE": {"blocks": [
                {
                    "opcode": "return (VALUE)",
                    "inputs": {
                        "VALUE": {"block": {
                            "opcode": "value of text [ARGUMENT]",
                            "options": {"ARGUMENT": ["value", "default"]},
                        }},
                    },
                },
            ]},
        },
    },
]}
