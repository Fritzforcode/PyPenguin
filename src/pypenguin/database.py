opcodeDatabase = {
# CATEGORIES
    # Motion
    # Looks
    # Sound
    # Events
    "event_whenkeypressed": {
        "type": "hat",
        "category": "events",
        "newOpcode": "when [KEY_OPTION] key pressed",
        "inputTypes": {},
        "optionTypes": {"KEY_OPTION": "key"}
    },
    "event_whenbroadcastreceived": {
        "type": "hat",
        "category": "events",
        "newOpcode": "when i receive [BROADCAST_OPTION]",
        "inputTypes": {},
        "optionTypes": {"BROADCAST_OPTION": "broadcast"}
    },
    "event_broadcast": {
        "type": "instruction",
        "category": "events",
        "newOpcode": "broadcast [BROADCAST_INPUT]",
        "inputTypes": {"BROADCAST_INPUT": "broadcast"},
        "optionTypes": {}
    },
    # Control
    # Sensing
    # Operators
    "operator_add": {
        "type": "textReporter",
        "category": "operators",
        "newOpcode": "(NUM1) + (NUM2)",
        "inputTypes": {"NUM1": "number", "NUM2": "number"},
        "optionTypes": {}
    },
    "operator_multiply": {
        "type": "textReporter",
        "category": "operators",
        "newOpcode": "(NUM1) * (NUM2)",
        "inputTypes": {"NUM1": "number", "NUM2": "number"},
        "optionTypes": {}
    },
    "operator_join": {
        "type": "textReporter",
        "category": "operators",
        "newOpcode": "join (STRING1) (STRING2)",
        "inputTypes": {"STRING1": "text", "STRING2": "text"},
        "optionTypes": {}
    },
    # Variables
    "data_setvariableto": {
        "type": "instruction",
        "category": "variables",
        "newOpcode": "set [VARIABLE] to (VALUE)",
        "inputTypes": {"VALUE": "text"},
        "optionTypes": {"VARIABLE": "variable"}
    },
    "data_changevariableby": {
        "type": "instruction",
        "category": "variables",
        "newOpcode": "change [VARIABLE] by (VALUE)",
        "inputTypes": {"VALUE": "number"},
        "optionTypes": {"VARIABLE": "variable"}
    },
    # Lists
    "data_addtolist" : {
        "type": "instruction",
        "category": "lists",
        "newOpcode": "add (ITEM) to [LIST]",
        "inputTypes": {"ITEM": "text"},
        "optionTypes": {"LIST": "list"}
    }   
# EXTENSIONS
    
}