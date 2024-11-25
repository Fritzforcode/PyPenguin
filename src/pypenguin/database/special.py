opcodes = {
# SPECIAL: Menus (DO NOT CREATE THESE MANUALLY; use their parent blocks)
    # Control
    "control_stop_sprite_menu": {
        "type": "menu",
        "category": "Control",
        "newOpcode": "#STOP SPRITE MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "control_create_clone_of_menu": { # menu for clone creation and deletion
        "type": "menu",
        "category": "Control",
        "newOpcode": "#CLONE TARGET MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "control_run_as_sprite_menu": {
        "type": "menu",
        "category": "Control",
        "newOpcode": "#RUN AS SPRITE MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    # Sensing
    "sensing_touchingobjectmenu": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#TOUCHING OBJECT MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_fulltouchingobjectmenu": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#FULL TOUCHING OBJECT MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_touchingobjectmenusprites": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#TOUCHING OBJECT MENU SPRITES",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_distancetomenu": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#DISTANCE TO MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
# SPECIAL: Variables and Lists
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
        #TODO: change return to VALUE
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