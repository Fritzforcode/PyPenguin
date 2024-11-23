opcodes = {
    "sensing_touchingobject": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "touching (OBJECT) ?",
        "inputTypes": {},
        "optionTypes": {"OBJECT": "mouse-pointer | edge"},
        "menu": {"new": "OBJECT", "old": "TOUCHINGOBJECTMENU", "menuOpcode": "sensing_touchingobjectmenu"},
    },
}