from helper_functions import readJSONFile, ikv, pp

opcodeDatabase = readJSONFile(filePath="assets/opcode_database.jsonc")
allowedOpcodes = [data["newOpcode"] for data in opcodeDatabase.values()]
textToSpeechLanguages = [
    None,
    "ar", "zh-cn", "da", "nl", "en", 
    "fr", "de", "hi", "is", "it", 
    "ja", "ko", "nb", "pl", "pt-br",
    "pt", "ro", "ru", "es", "es-419", 
    "sv", "tr", "cy",
] # language abbreviations

commentSchema = {
    "type": ["object", "null"],
    "properties": {
        "position": {
            "type"    : "array",
            "items"   : {"type": ["number", "integer"]},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
            "additionalItems": False,
        },
        "minimized": {"type": "boolean"},
        "text"     : {"type": "string"},
    },
    "required": ["position", "size", "minimized", "text"],
}
blockSchema = {
    "type": "object",
    "properties": {
        "opcode" : {"type": "string", "enum": allowedOpcodes},
        "inputs" : {"type": "object"},
        "options": {"type": "object"},
        "comment": commentSchema,
    },
    "required": ["opcode", "inputs", "options", "comment"],
}
scriptSchema = {
        "type": "object",
        "properties": {
            "position"    : {
                "type"    : "array",
                "items"   : {"type": "integer"},
                "minItems": 2,
                "maxItems": 2,
            },
            "blocks": {"type": "array", "items": blockSchema},
        },
        "required": ["position", "blocks"],
}
costumeSchema = {
    "type": "object",
    "properties": {
        "name"            : {"type": "string"},
        "bitmapResolution": {"type": "integer", "minimum": 1},
        "dataFormat"      : {"type": "string"},
        "fileStem"        : {"type": "string"},
        "rotationCenter": {
            "type": "array",
            "items"   : {"type": ["integer", "number"]},
            "minItems": 2,
            "maxItems": 2,
 
        },
    },
    "required": ["name", "dataFormat", "fileStem", "rotationCenter"],

}
soundSchema = {
    "type": "object",
    "properties": {
        "name"       : {"type": "string"},
        "dataFormat" : {"type": "string"},
        "fileStem"   : {"type": "string"},
        "rate"       : {"type": "integer"},
        "sampleCount": {"type": "integer"},
    },
    "required": ["name", "dataFormat", "fileStem", "rate", "sampleCount"],
}
stageSchema = {
    "type": "object",
    "properties": {
        # stage version
        "isStage": {"type": "boolean", "const": True},
        "name"   : {"type": "string", "const": "Stage"},
        # common
        "scripts"       : {"type": "array", "items": scriptSchema},
        "comments"      : {"type": "array", "items": commentSchema},
        "currentCostume": {"type": "integer", "minimum":0},
        "costumes"      : {"type": "array", "items": costumeSchema},
        "sounds"        : {"type": "array", "items": soundSchema},
        "volume"        : {"type": ["integer", "number"], "minimum": 0, "maximum": 100},
        # stage version
        "layerOrder"    : {"type": "integer", "const": 0},
    },        
    "required": [
        "isStage", "name", "scripts", "comments", "currentCostume", 
        "costumes", "sounds", "volume", "layerOrder",
    ],
}
spriteSchema = {
    "type": "object",
    "properties": {
        # sprite version
        "isStage": {"type": "boolean"},
        "name"   : {"type": "string"},
        # common
        "scripts"       : {"type": "array", "items": scriptSchema},
        "comments"      : {"type": "array", "items": commentSchema},
        "currentCostume": {"type": "integer", "minimum":0},
        "costumes"      : {"type": "array", "items": costumeSchema},
        "sounds"        : {"type": "array", "items": soundSchema},
        "volume"        : {"type": ["integer", "number"], "minimum": 0, "maximum": 100},
        # sprite version
        "layerOrder"    : {"type": "integer", "minimum": 0},
        # sprite only
        "visible": {"type": "boolean"},
        "position": {
            "type": "array",
            "items": {"type": ["integer", "number"]},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {"type": ["integer", "number"]}, 
        "direction": {"type": ["integer", "number"]}, 
        "draggable": {"type": "boolean"},
        "rotationStyle": {"type": "string", "enum": ["all around", "left-right", "don't rotate"]}, 
    },        
    "required": [
        "isStage", "name", "scripts", "comments", "currentCostume", 
        "costumes", "sounds", "volume", "layerOrder", 
#"visible", "position", "size", "direction", "draggable", "rotationStyle"
    ],
}
variableMonitorSchema = {
    "type": ["object", "null"],
    "properties": {
        "visible": {"type": "boolean"},
        "size"   : {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "position": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "sliderMin"   : {"type": ["integer", "number"]},
        "sliderMax"   : {"type": ["integer", "number"]},
        "onlyIntegers": {"type": "boolean"},
    },
    "required": ["visible", "size", "position", "sliderMin", "sliderMax", "onlyIntegers"],
}
variableSchema = {
    "type": "object",
    "properties": {
        "name"        : {"type": "string"},
        "currentValue": {"type": ["string", "integer", "number"]}, 
        "mode"        : {"type": "string", "enum": ["cloud", "global", "local"]},
        "sprite"      : {"type": ["string", "null"]},
        "monitor"     : variableMonitorSchema,
    },
    "required": ["name", "currentValue", "mode", "sprite", "monitor"],
}
listMonitorSchema = {
    "type": ["object", "null"],
    "properties": {
        "visible": {"type": "boolean"},
        "size"   : {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "position": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
    },
    "required": ["visible", "size", "position"],
}
listSchema = {
    "type": "object",
    "properties": {
        "name"        : variableSchema["properties"]["name"],
        "currentValue": {"type": "array", "items": variableSchema["properties"]["currentValue"]},
        "mode"        : {"type": "string", "enum": ["global", "local"]},
        "sprite"      : variableSchema["properties"]["sprite"],
        "monitor"     : listMonitorSchema,
    },
    "required": ["name", "currentValue", "mode", "sprite", "monitor"],
}   
metaSchema = {
    "type": "object",
    "properties": {
        "semver": {"type": "string"},
        "vm"    : {"type": "string"},
        "agent" : {"type": "string"},
        "platform": {
            "name"   : {"type": "string"},
            "url"    : {"type": "string"},
            "version": {"type": "string"},
        },
    },
}
projectSchema = {
    "type": "object",
    "properties": {
        "sprites"             : {"type": "array", "items": spriteSchema,  "minItems": 1},
        "variables"           : {"type": "array", "items": variableSchema},
        "lists"               : {"type": "array", "items": listSchema},
        "tempo"               : {"type": "integer", "minimum": 20, "maximum": 500},
        "videoTransparency"   : {"type": ["integer", "number"]}, # i found no limits
        "videoState"          : {"type": "string", "enum": ["on", "on flipped", "off"]},
        "textToSpeechLanguage": {"type": ["null", "string"], "enum": textToSpeechLanguages},
        "extensionData"       : {"type": "object"}, # Will not be checked, needs further research to be checked
        "extensions"          : {"type": "array"},  # /\<< 
        "meta"                : metaSchema,
    },
    "required": [
        "sprites", "variables", "lists", "extensionData", "extensions", 
        "meta", "tempo", "videoTransparency", "videoState", "textToSpeechLanguage",
    ],
}
