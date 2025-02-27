opcodes = {
    "motion_movesteps": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "move (STEPS) steps",
        "inputTypes": {"STEPS": "number"},
        "optionTypes": {},
    },
    "motion_movebacksteps": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "move back (STEPS) steps",
        "inputTypes": {"STEPS": "number"},
        "optionTypes": {},
        "fromPenguinMod": True,
    },
    "motion_moveupdownsteps": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "move [DIRECTION] (STEPS) steps",
        "inputTypes": {"STEPS": "number"},
        "optionTypes": {"DIRECTION": "up|down"},
        "fromPenguinMod": True,
    },
    "motion_turnright": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "turn clockwise (DEGREES) degrees",
        "inputTypes": {"DEGREES": "number"},
        "optionTypes": {},
    },
    "motion_turnleft": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "turn counterclockwise (DEGREES) degrees",
        "inputTypes": {"DEGREES": "number"},
        "optionTypes": {},
    },
    "motion_goto": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "go to ([TARGET])",
        "inputTypes": {"TARGET": "random|mouse || other sprite"},
        "optionTypes": {},
        "menus": [{"new": "TARGET", "outer": "TO", "inner": "TO", "menuOpcode":  "motion_goto_menu"}],
    },
    "motion_gotoxy": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "go to x: (X) y: (Y)",
        "inputTypes": {"X": "number", "Y": "number"},
        "optionTypes": {},
    },
    "motion_changebyxy": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "change by x: (DX) y: (DY)",
        "inputTypes": {"DX": "number", "DY": "number"},
        "optionTypes": {},
        "fromPenguinMod": True,
    },
    "motion_glideto": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "glide (SECONDS) secs to ([TARGET])",
        "inputTypes": {"SECONDS": "number", "TARGET": "random|mouse || other sprite"},
        "inputTranslation": {"SECS": "SECONDS"},
        "optionTypes": {},
        "menus": [{"new": "TARGET", "outer": "TO", "inner": "TO", "menuOpcode":  "motion_glideto_menu"}],
    },
    "motion_glidesecstoxy": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "glide (SECONDS) secs to x: (X) y: (Y)",
        "inputTypes": {"SECONDS": "number", "X": "number", "Y": "number"},
        "inputTranslation": {"SECS": "SECONDS"},
        "optionTypes": {},
    },
    "motion_pointindirection": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "point in direction (DIRECTION)",
        "inputTypes": {"DIRECTION": "direction"},
        "optionTypes": {},
    },
    "motion_pointtowards": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "point towards ([TARGET])",
        "inputTypes": {"TARGET": "random|mouse || other sprite"},
        "optionTypes": {},
        "menus": [{"new": "TARGET", "outer": "TOWARDS", "inner": "TOWARDS", "menuOpcode":  "motion_glideto_menu"}],
    },
    "motion_pointtowardsxy": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "point towards x: (X) y: (Y)",
        "inputTypes": {"X": "number", "Y": "number"},
        "optionTypes": {},
        "fromPenguinMod": True,
    },
    "motion_turnaround": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "turn around",
        "inputTypes": {},
        "optionTypes": {},
        "fromPenguinMod": True,
    },
    "motion_changexby": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "change x by (DX)",
        "inputTypes": {"DX": "number"},
        "optionTypes": {},
    },
    "motion_setx": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "set x to (X)",
        "inputTypes": {"X": "number"},
        "optionTypes": {},
    },
    "motion_changeyby": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "change y by (DY)",
        "inputTypes": {"DY": "number"},
        "optionTypes": {},
    },
    "motion_sety": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "set y to (Y)",
        "inputTypes": {"Y": "number"},
        "optionTypes": {},
    },
    "motion_ifonedgebounce": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "if on edge, bounce",
        "inputTypes": {},
        "optionTypes": {},
    },
    "motion_ifonspritebounce": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "if touching ([TARGET]), bounce",
        "inputTypes": {"TARGET": "random|mouse || other sprite"},
        "optionTypes": {},
        "menus": [{"new": "TARGET", "outer": "SPRITE", "inner": "TOWARDS", "menuOpcode": "motion_pointtowards_menu"}],
        "fromPenguinMod": True,
    },
    "motion_setrotationstyle": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "set rotation style [STYLE]",
        "inputTypes": {},
        "optionTypes": {"STYLE": "rotation style"},
    },
    "motion_move_sprite_to_scene_side": {
        "type": "instruction",
        "category": "Motion",
        "newOpcode": "move to stage [ZONE]",
        "inputTypes": {},
        "optionTypes": {"ZONE": "stage zone"},
        "optionTranslation": {"ALIGNMENT": "ZONE"},
        "fromPenguinMod": True,
    },
    "motion_xposition": {
        "type": "stringReporter",
        "category": "Motion",
        "newOpcode": "x position",
        "inputTypes": {},
        "optionTypes": {},
        "canHaveMonitor": True,
    },
    "motion_yposition": {
        "type": "stringReporter",
        "category": "Motion",
        "newOpcode": "y position",
        "inputTypes": {},
        "optionTypes": {},
        "canHaveMonitor": True,
    },
    "motion_direction": {
        "type": "stringReporter",
        "category": "Motion",
        "newOpcode": "direction",
        "inputTypes": {},
        "optionTypes": {},
        "canHaveMonitor": True,
    },
}