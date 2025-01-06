voidValue =     {
    "position": [-1000, 0],
    "blocks": [
        {
            "opcode": "define custom block",
            "options": {
                "noScreenRefresh": ["value", True], 
                "blockType": ["value", "instruction"], 
                "customOpcode": ["value", "VOID (value)"],
            },
        },
        {
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {"VALUE": {"block": {
                "opcode": "value of text [ARGUMENT]",
                "options": {"ARGUMENT": ["value", "value"]},
            }}},
            "options": {"VARIABLE": ["variable", "__VOID__"]},
        },
    ]
}
