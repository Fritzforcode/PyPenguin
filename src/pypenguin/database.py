opcodeDatabase = {
# CATEGORIES
    # Motion
    # Looks
    # Sound
    # Events
    "event_whenkeypressed": {
        "type": "hat",
        "category": "Events",
        "newOpcode": "when [KEY_OPTION] key pressed",
        "inputTypes": {},
        "optionTypes": {"KEY_OPTION": "key"}
    },
    "event_whenbroadcastreceived": {
        "type": "hat",
        "category": "Events",
        "newOpcode": "when i receive [BROADCAST_OPTION]",
        "inputTypes": {},
        "optionTypes": {"BROADCAST_OPTION": "broadcast"}
    },
    "event_broadcast": {
        "type": "instruction",
        "category": "Events",
        "newOpcode": "broadcast [BROADCAST_INPUT]",
        "inputTypes": {"BROADCAST_INPUT": "broadcast"},
        "optionTypes": {}
    },
    # Control
    "control_if": {
        "type": "instruction",
        "category": "Control",
        "newOpcode": "if <CONDITION> then {SUBSTACK}",
        "inputTypes": {"CONDITION": "boolean", "SUBSTACK": "script"},
        "optionTypes": {}
    },
    "control_if_else": {
        "type": "instruction",
        "category": "Control",
        "newOpcode": "if <CONDITION> then {SUBSTACK} else {SUBSTACK2}",
        "inputTypes": {"CONDITION": "boolean", "SUBSTACK": "script", "SUBSTACK2": "script"},
        "optionTypes": {}
    },
    # Sensing
    # Operators
    "operator_add": {
        "type": "textReporter",
        "category": "Operators",
        "newOpcode": "(NUM1) + (NUM2)",
        "inputTypes": {"NUM1": "number", "NUM2": "number"},
        "optionTypes": {}
    },
    "operator_multiply": {
        "type": "textReporter",
        "category": "Operators",
        "newOpcode": "(NUM1) * (NUM2)",
        "inputTypes": {"NUM1": "number", "NUM2": "number"},
        "optionTypes": {}
    },
    "operator_join": {
        "type": "textReporter",
        "category": "Operators",
        "newOpcode": "join (STRING1) (STRING2)",
        "inputTypes": {"STRING1": "text", "STRING2": "text"},
        "optionTypes": {}
    },
    "operator_trueBoolean": {
        "type": "booleanReporter",
        "category": "Operators",
        "newOpcode": "true",
        "inputTypes": {},
        "optionTypes": {}
    },
    "operator_falseBoolean": {
        "type": "booleanReporter",
        "category": "Operators",
        "newOpcode": "false",
        "inputTypes": {},
        "optionTypes": {}
    },
    # Variables
    "data_setvariableto": {
        "type": "instruction",
        "category": "Variables",
        "newOpcode": "set [VARIABLE] to (VALUE)",
        "inputTypes": {"VALUE": "text"},
        "optionTypes": {"VARIABLE": "variable"}
    },
    "data_changevariableby": {
        "type": "instruction",
        "category": "Variables",
        "newOpcode": "change [VARIABLE] by (VALUE)",
        "inputTypes": {"VALUE": "number"},
        "optionTypes": {"VARIABLE": "variable"}
    },
    # Lists
    "data_addtolist" : {
        "type": "instruction",
        "category": "Lists",
        "newOpcode": "add (ITEM) to [LIST]",
        "inputTypes": {"ITEM": "text"},
        "optionTypes": {"LIST": "list"}
    },
# EXTENSIONS
    # JSON (jgJSON)
    "jgJSON_getValueFromJSON": {
        "type": "textReporter",
        "category": "JSON",
        "newOpcode": "get (VALUE) from (JSON)",
        "inputTypes": {"VALUE": "text", "JSON": "text"},
        "optionTypes": {}
    },
    "jgJSON_setValueToKeyInJSON": {
        "type": "textReporter",
        "category": "JSON",
        "newOpcode": "set (KEY) to (VALUE) in (JSON)",
        "inputTypes": {"KEY": "text", "VALUE": "text", "JSON": "text"},
        "optionTypes": {}
    },
    "jgJSON_json_array_push": {
        "type": "textReporter",
        "category": "JSON",
        "newOpcode": "in array (array) add (item)",
        "inputTypes": {"array": "text", "item": "text"},
        "optionTypes": {}
    },
    "jgJSON_json_array_get": {
        "type": "textReporter",
        "category": "JSON",
        "newOpcode": "in array (array) get (index)",
        "inputTypes": {"array": "text", "index": "text"},
        "optionTypes": {}
    },
# SPECIAL
    "special_variable_value": {
        "type": "textReporter",
        "category": "Variables",
        "newOpcode": "VARIABLE",
        "inputTypes": {},
        "optionTypes": {"VARIABLE": "variable"}
    },
    "special_list_value": {
        "type": "textReporter",
        "category": "Lists",
        "newOpcode": "LIST",
        "inputTypes": {},
        "optionTypes": {"LIST": "list"}
    },
    "special_define": {
        "type": "hat",
        "category": "My Blocks",
        "newOpcode": "define ...",
        "inputTypes": {},
        "optionTypes": {"noScreenRefresh": "boolean", "blockType": "blockType", "id": "integer"}
    },
    "procedures_call": {
        "type": "dynamic",
        "category": "My Blocks",
        "newOpcode": "call ...",
        "inputTypes": {},
        "optionTypes": {"blockDef": "customBlockId"},
    },
}