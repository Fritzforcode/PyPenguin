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
    "control_if": {
        "type": "instruction",
        "category": "control",
        "newOpcode": "if <CONDITION> then {SUBSTACK}",
        "inputTypes": {"CONDITION": "boolean", "SUBSTACK": "script"},
        "optionTypes": {}
    },
    "control_if_else": {
        "type": "instruction",
        "category": "control",
        "newOpcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
        "inputTypes": {"CONDITION": "boolean", "SUBSTACK": "script", "SUBSTACK2": "script"},
        "optionTypes": {}
    },
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
    "operator_trueBoolean": {
        "type": "booleanReporter",
        "category": "operators",
        "newOpcode": "true",
        "inputTypes": {},
        "optionTypes": {}
    },
    "operator_falseBoolean": {
        "type": "booleanReporter",
        "category": "operators",
        "newOpcode": "false",
        "inputTypes": {},
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
    },
# EXTENSIONS
    # JSON (jgJSON)
    "jgJSON_getValueFromJSON": {
        "type": "textReporter",
        "category": "json",
        "newOpcode": "get (VALUE) from (JSON)",
        "inputTypes": {"VALUE": "text", "JSON": "text"},
        "optionTypes": {}
    },
    "jgJSON_setValueToKeyInJSON": {
        "type": "textReporter",
        "category": "json",
        "newOpcode": "set (KEY) to (VALUE) in (JSON)",
        "inputTypes": {"KEY": "text", "VALUE": "text", "JSON": "text"},
        "optionTypes": {}
    },
    "jgJSON_json_array_push": {
        "type": "textReporter",
        "category": "json",
        "newOpcode": "in array (array) add (item)",
        "inputTypes": {"array": "text", "item": "text"},
        "optionTypes": {}
    },
    "jgJSON_json_array_get": {
        "type": "textReporter",
        "category": "json",
        "newOpcode": "in array (array) get (index)",
        "inputTypes": {"array": "text", "index": "text"},
        "optionTypes": {}
    },
# SPECIAL
    "special_variable_value": {
        "type": "textReporter",
        "category": "variables",
        "newOpcode": "VARIABLE",
        "inputTypes": {},
        "optionTypes": {"VARIABLE": "variable"}
    },
    "special_list_value": {
        "type": "textReporter",
        "category": "lists",
        "newOpcode": "LIST",
        "inputTypes": {},
        "optionTypes": {"LIST": "list"}
    },

}