opcodes = {
    "lmsTempVars2_setThreadVariable": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "set thread var (VARIABLE) to (VALUE)",
        "inputTypes": {"VARIABLE": "text", "VALUE": "text"},
        "inputTranslation": {"VAR": "VARIABLE", "STRING": "VALUE"},
        "optionTypes": {},
    },
    "lmsTempVars2_changeThreadVariable": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "change thread var (VARIABLE) by (VALUE)",
        "inputTypes": {"VARIABLE": "text", "VALUE": "text"},
        "inputTranslation": {"VAR": "VARIABLE", "NUM": "VALUE"},
        "optionTypes": {},
    },
    "lmsTempVars2_getThreadVariable": {
        "type": "stringReporter",
        "category": "Temporary Variables",
        "newOpcode": "thread var (VARIABLE)",
        "inputTypes": {"VARIABLE": "text"},
        "inputTranslation": {"VAR": "VARIABLE"},
        "optionTypes": {},
    },
    "lmsTempVars2_threadVariableExists": {
        "type": "booleanReporter",
        "category": "Temporary Variables",
        "newOpcode": "thread var (VARIABLE) exists?",
        "inputTypes": {"VARIABLE": "text"},
        "inputTranslation": {"VAR": "VARIABLE"},
        "optionTypes": {},
    },
    "lmsTempVars2_forEachThreadVariable": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "for (VARIABLE) in (COUNT) {BODY}",
        "inputTypes": {"VARIABLE": "text", "COUNT": "number"},
        "inputTranslation": {"VAR": "VARIABLE", "NUM": "COUNT"},
        "optionTypes": {},
    },
    "lmsTempVars2_listThreadVariables": {
        "type": "stringReporter",
        "category": "Temporary Variables",
        "newOpcode": "active thread variables",
        "inputTypes": {},
        "optionTypes": {},
    },
    "lmsTempVars2_setRuntimeVariable": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "set runtime var (VARIABLE) to (VALUE)",
        "inputTypes": {"VARIABLE": "text", "VALUE": "text"},
        "inputTranslation": {"VAR": "VARIABLE", "STRING": "VALUE"},
        "optionTypes": {},
    },
    "lmsTempVars2_changeRuntimeVariable": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "change runtime var (VARIABLE) by (VALUE)",
        "inputTypes": {"VARIABLE": "text", "VALUE": "text"},
        "inputTranslation": {"VAR": "VARIABLE", "NUM": "VALUE"},
        "optionTypes": {},
    },
    "lmsTempVars2_getRuntimeVariable": {
        "type": "stringReporter",
        "category": "Temporary Variables",
        "newOpcode": "runtime var (VARIABLE)",
        "inputTypes": {"VARIABLE": "text"},
        "inputTranslation": {"VAR": "VARIABLE"},
        "optionTypes": {},
    },
    "lmsTempVars2_runtimeVariableExists": {
        "type": "booleanReporter",
        "category": "Temporary Variables",
        "newOpcode": "runtime var (VARIABLE) exists?",
        "inputTypes": {"VARIABLE": "text"},
        "inputTranslation": {"VAR": "VARIABLE"},
        "optionTypes": {},
    },
    "lmsTempVars2_deleteRuntimeVariable": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "delete runtime var (VARIABLE)",
        "inputTypes": {"VARIABLE": "text"},
        "inputTranslation": {"VAR": "VARIABLE"},
        "optionTypes": {},
    },
    "lmsTempVars2_deleteAllRuntimeVariables": {
        "type": "instruction",
        "category": "Temporary Variables",
        "newOpcode": "delete all runtime variables",
        "inputTypes": {},
        "optionTypes": {},
    },
    "lmsTempVars2_listRuntimeVariables": {
        "type": "stringReporter",
        "category": "Temporary Variables",
        "newOpcode": "active runtime variables",
        "inputTypes": {},
        "optionTypes": {},
    },
}