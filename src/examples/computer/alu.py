excecuteAluInstrDef = {
    "position": [500,0],
    "blocks": [
        {
            "opcode": "define ...",
            "options": {
                "noScreenRefresh": True,
                "blockType": "instruction",
                "customOpcode": "execute alu instr (instr)",
            }
        },
        {
            "opcode": "switch (CONDITION) {SUBSTACK1} default {SUBSTACK2}",
            "inputs": {
                "CONDITION": {
                    "opcode": "value of text argument [VALUE]",
                },
            },
        },
    ],
}