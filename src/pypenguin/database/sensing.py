opcodes = {
    "sensing_touchingobject": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "touching ([OBJECT]) ?",
        "inputTypes": {"OBJECT": "half-inclusive touchable object"},
        "inputTranslation": {"TOUCHINGOBJECTMENU": "OBJECT"},
        "optionTypes": {},
        "menus": [{"new": "OBJECT", "outer": "TOUCHINGOBJECTMENU", "inner": "TOUCHINGOBJECTMENU", "menuOpcode": "sensing_touchingobjectmenu"}],
    },
    "sensing_objecttouchingobject": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "([OBJECT]) touching ([SPRITE]) ?",
        "inputTypes": {"OBJECT": "inclusive touchable object", "SPRITE": "touchable sprite"},
        "optionTypes": {},
        "menus": [
            {"new": "OBJECT", "outer": "FULLTOUCHINGOBJECTMENU",   "inner": "FULLTOUCHINGOBJECTMENU",   "menuOpcode": "sensing_fulltouchingobjectmenu"   },
            {"new": "SPRITE", "outer": "SPRITETOUCHINGOBJECTMENU", "inner": "SPRITETOUCHINGOBJECTMENU", "menuOpcode": "sensing_touchingobjectmenusprites"},
        ],
    },
    "sensing_objecttouchingclonesprite": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "([OBJECT]) touching clone of ([SPRITE]) ?",
        "inputTypes": {"OBJECT": "inclusive touchable object", "SPRITE": "touchable sprite"},
        "optionTypes": {},
        "menus": [
            {"new": "OBJECT", "outer": "FULLTOUCHINGOBJECTMENU",   "inner": "FULLTOUCHINGOBJECTMENU",   "menuOpcode": "sensing_fulltouchingobjectmenu"   },
            {"new": "SPRITE", "outer": "SPRITETOUCHINGOBJECTMENU", "inner": "SPRITETOUCHINGOBJECTMENU", "menuOpcode": "sensing_touchingobjectmenusprites"},
        ],
    },
    "sensing_touchingcolor": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "touching color (COLOR) ?",
        "inputTypes": {"COLOR": "color"},
        "optionTypes": {},
    },
    "sensing_coloristouchingcolor": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "color (COLOR1) is touching color (COLOR2) ?",
        "inputTypes": {"COLOR1": "color", "COLOR2": "color"},
        "inputTranslation": {"COLOR": "COLOR1"},
        "optionTypes": {},
    },
    "sensing_getxyoftouchingsprite": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "[COORDINATE] of touching ([OBJECT]) point",
        "inputTypes": {"OBJECT": "exclusive touchable object"},
        "optionTypes": {"COORDINATE": "coordinate"},
        "optionTranslation": {"XY": "COORDINATE"},
        "menus": [{"new": "OBJECT", "outer": "SPRITE", "inner": "DISTANCETOMENU", "menuOpcode": "sensing_distancetomenu"}],
    },
    "sensing_distanceto": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "distance to ([OBJECT])",
        "inputTypes": {"OBJECT": "exclusive touchable object"},
        "optionTypes": {},
        "menus": [{"new": "OBJECT", "outer": "DISTANCETOMENU", "inner": "DISTANCETOMENU", "menuOpcode": "sensing_distancetomenu"}],
    },
    "sensing_distanceTo": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "distance from (X1) (Y1) to (X2) (Y2)",
        "inputTypes": {
            "X1": "text", "Y1": "text",
            "X2": "text", "Y2": "text",
        },
        "inputTranslation": {"x1": "X1", "y1": "Y1", "x2": "X2", "y2": "Y2"},
        "optionTypes": {},
    },
    "sensing_directionTo": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "direction to (X1) (Y1) from (X2) (Y2)",
        "inputTypes": {
            "X1": "text", "Y1": "text",
            "X2": "text", "Y2": "text",
        },
        "inputTranslation": {"x2": "X1", "y2": "Y1", "x1": "X2", "y1": "Y2"},
        "optionTypes": {},
    },
    "sensing_askandwait": {
        "type": "instruction",
        "category": "Sensing",
        "newOpcode": "ask (QUESTION) and wait",
        "inputTypes": {"QUESTION": "text"},
        "optionTypes": {},
    },
    "sensing_answer": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "answer",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_thing_is_text": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "(STRING) is text?",
        "inputTypes": {"STRING": "text"},
        "inputTranslation": {"TEXT1": "STRING"},
        "optionTypes": {},
    },
    "sensing_thing_is_number": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "(STRING) is number?",
        "inputTypes": {"STRING": "text"},
        "inputTranslation": {"TEXT1": "STRING"},
        "optionTypes": {},
    },
    "sensing_keypressed": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "key ([KEY]) pressed?",
        "inputTypes": {"KEY": "key"},
        "optionTypes": {},
        "menus": [{"new": "KEY", "outer": "KEY_OPTION", "inner": "KEY_OPTION", "menuOpcode": "sensing_keyoptions"}],
    },
    "sensing_keyhit": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "key ([KEY]) hit?",
        "inputTypes": {"KEY": "key"},
        "optionTypes": {},
        "menus": [{"new": "KEY", "outer": "KEY_OPTION", "inner": "KEY_OPTION", "menuOpcode": "sensing_keyoptions"}],
    },
    "sensing_mousescrolling": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "is mouse scrolling ([DIRECTION]) ?",
        "inputTypes": {"DIRECTION": "up or down"},
        "optionTypes": {},
        "menus": [{"new": "DIRECTION", "outer": "SCROLL_OPTION", "inner": "SCROLL_OPTION", "menuOpcode": "sensing_scrolldirections"}],
    },
    "sensing_mousedown": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "mouse down?",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_mouseclicked": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "mouse clicked?",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_mousex": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "mouse x",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_mousey": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "mouse y",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_setclipboard": {
        "type": "instruction",
        "category": "Sensing",
        "newOpcode": "add (TEXT) to clipboard",
        "inputTypes": {"TEXT": "text"},
        "inputTranslation": {"ITEM": "TEXT"},
        "optionTypes": {},
    },
    "sensing_getclipboard": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "clipboard item",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_setdragmode": {
        "type": "instruction",
        "category": "Sensing",
        "newOpcode": "set drag mode [MODE]",
        "inputTypes": {},
        "optionTypes": {"MODE": "drag mode"},
        "optionTranslation": {"DRAG_MODE": "MODE"},
    },
    "sensing_getdragmode": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "draggable?",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_loudness": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "loudness",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_loud": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "loud?",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_resettimer": {
        "type": "instruction",
        "category": "Sensing",
        "newOpcode": "reset timer",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_timer": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "timer",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_set_of": {
        "type": "instruction",
        "category": "Sensing",
        "newOpcode": "set [PROPERTY] of ([TARGET]) to (VALUE)",
        "inputTypes": {"VALUE": "text", "TARGET": "other sprite or stage"},
        "optionTypes": {"PROPERTY": "mutable sprite property"},
        "menus": [{"new": "TARGET", "outer": "OBJECT", "inner": "OBJECT", "menuOpcode": "sensing_of_object_menu"}],
    },
    "sensing_of": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "[PROPERTY] of ([TARGET])",
        "inputTypes": {"TARGET": "other sprite or stage"},
        "optionTypes": {"PROPERTY": "readable sprite property"},
        "menus": [{"new": "TARGET", "outer": "OBJECT", "inner": "OBJECT", "menuOpcode": "sensing_of_object_menu"}],
    },
    "sensing_current": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "current [PROPERTY]",
        "inputTypes": {},
        "optionTypes": {"PROPERTY": "time property"},
        "optionTranslation": {"CURRENTMENU": "PROPERTY"},
    },
    "sensing_dayssince2000": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "days since 2000",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_mobile": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "mobile?",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_fingerdown": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "finger ([INDEX]) down?",
        "inputTypes": {"INDEX": "finger index"},
        "optionTypes": {},
        "menus": [{"new": "INDEX", "outer": "FINGER_OPTION", "inner": "FINGER_OPTION", "menuOpcode": "sensing_fingeroptions"}],
    },
    "sensing_fingertapped": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "finger ([INDEX]) tapped?",
        "inputTypes": {"INDEX": "finger index"},
        "optionTypes": {},
        "menus": [{"new": "INDEX", "outer": "FINGER_OPTION", "inner": "FINGER_OPTION", "menuOpcode": "sensing_fingeroptions"}],
    },
    "sensing_fingerx": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "finger ([INDEX]) x",
        "inputTypes": {"INDEX": "finger index"},
        "optionTypes": {},
        "menus": [{"new": "INDEX", "outer": "FINGER_OPTION", "inner": "FINGER_OPTION", "menuOpcode": "sensing_fingeroptions"}],
    },
    "sensing_fingery": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "finger ([INDEX]) y",
        "inputTypes": {"INDEX": "finger index"},
        "optionTypes": {},
        "menus": [{"new": "INDEX", "outer": "FINGER_OPTION", "inner": "FINGER_OPTION", "menuOpcode": "sensing_fingeroptions"}],
    },
    "sensing_username": {
        "type": "stringReporter",
        "category": "Sensing",
        "newOpcode": "username",
        "inputTypes": {},
        "optionTypes": {},
    },
    "sensing_loggedin": {
        "type": "booleanReporter",
        "category": "Sensing",
        "newOpcode": "logged in?",
        "inputTypes": {},
        "optionTypes": {},
    },
}