opcodes = {
# SPECIAL: Menus (DO NOT CREATE THESE MANUALLY; use their parent blocks)
    "control_stop_sprite_menu": {
        "type": "textReporter",
        "category": "Control",
        "newOpcode": "STOP SPRITE MENU",
        "inputTypes": {},
        "optionTypes": {"TARGET": "cloning target"},
    },
    "control_create_clone_of_menu": { # menu for clone creation and deletion
        "type": "textReporter",
        "category": "Control",
        "newOpcode": "CLONE TARGET MENU",
        "inputTypes": {},
        "optionTypes": {"TARGET": "cloning target"},
    },
    "control_run_as_sprite_menu": {
        "type": "textReporter",
        "category": "Control",
        "newOpcode": "",
        "inputTypes": {},
        "optionTypes": {"TARGET": ""},
    },
# SPECIAL: Varibles and Lists
    "special_variable_value": {
        "type": "textReporter",
        "category": "Variables",
        "newOpcode": "value of [VARIABLE]",
        "inputTypes": {},
        "optionTypes": {"VARIABLE": "variable"},
    },
    "special_list_value": {
        "type": "textReporter",
        "category": "Lists",
        "newOpcode": "value of [LIST]",
        "inputTypes": {},
        "optionTypes": {"LIST": "list"},
    },
# SPECIAL: Custom Blocks
    "special_define": {
        "type": "hat",
        "category": "My Blocks",
        "newOpcode": "define ...",
        "inputTypes": {},
        "optionTypes": {"noScreenRefresh": "boolean", "blockType": "blockType", "customOpcode": "opcode"},
    },
    "procedures_call": {
        "type": "dynamic",
        "category": "My Blocks",
        "newOpcode": "call ...",
        "inputTypes": {},
        "optionTypes": {"customOpcode": "opcode"},
    },
    "procedures_return": {
        "type": "lastInstruction",
        "category": "My Blocks",
        "newOpcode": "return (return)",
        "inputTypes": {"return": "text"},
        "optionTypes": {},
    },
    "procedures_set": {
        "type": "instruction",
        "category": "My Blocks",
        "newOpcode": "set (PARAM) to (VALUE)",
        "inputTypes": {"PARAM": "round", "VALUE": "text"},
        "optionTypes": {},
    },
    "argument_reporter_string_number": {
        "type": "textReporter",
        "category": None,
        "newOpcode": "value of text [ARGUMENT]",
        "inputTypes": {},
        "optionTypes": {"ARGUMENT": "string"},
        "optionTranslation": {"VALUE": "ARGUMENT"},
    },
    "argument_reporter_boolean": {
        "type": "booleanReporter",
        "category": None,
        "newOpcode": "value of boolean [ARGUMENT]",
        "inputTypes": {},
        "optionTypes": {"ARGUMENT": "string"},
        "optionTranslation": {"VALUE": "ARGUMENT"},
    },
}