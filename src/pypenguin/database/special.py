opcodes = {
# SPECIAL: Menus (DO NOT CREATE THESE MANUALLY; they are created automatically when needed)
    # Motion
    "motion_goto_menu": {
        "type": "menu",
        "category": "Motion",
        "newOpcode": "#REACHABLE TARGET MENU (GO)",
        "inputTypes": {},
        "optionTypes": {},
    },
    "motion_glideto_menu": {
        "type": "menu",
        "category": "Motion",
        "newOpcode": "#REACHABLE TARGET MENU (GLIDE)",
        "inputTypes": {},
        "optionTypes": {},
    },
    "motion_pointtowards_menu": {
        "type": "menu",
        "category": "Motion",
        "newOpcode": "#OBSERVABLE TARGET MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
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
    "sensing_keyoptions": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#KEY MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_scrolldirections": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#SCROLL DIRECTION MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_of_object_menu": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#OJBECT PROPERTY MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_fingeroptions": {
        "type": "menu",
        "category": "Sensing",
        "newOpcode": "#FINGER INDEX MENU",
        "inputTypes": {},
        "optionTypes": {},
    },
# SPECIAL: Variables and Lists
    "special_variable_value": {
        "type": "stringReporter",
        "category": "Variables",
        "newOpcode": "value of [VARIABLE]",
        "inputTypes": {},
        "optionTypes": {"VARIABLE": "variable"},
    },
    "special_list_value": {
        "type": "stringReporter",
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
        "newOpcode": "return (VALUE)",
        "inputTypes": {"VALUE": "text"},
        "inputTranslation": {"return": "VALUE"},
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
        "type": "stringReporter",
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