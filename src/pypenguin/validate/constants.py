from pypenguin.database import getAllMonitorOpcodes#, getAllOptimizedOpcodes
from pypenguin.validate.errors import *

allowedMenuOpcodes = getAllMonitorOpcodes()
textToSpeechLanguages = [
    None,
    "Arabic (ar)", "Chinese (Mandarin) (zh-cn)", "Danish (da)", "Dutch (nl)", "English (en)", 
    "French (fr)", "German (de)", "Hindi (hi)", "Icelandic (is)", "Italian (it)", 
    "Japanese (ja)", "Korean (ko)", "Norwegian (nb)", "Polish (pl)", "Portuguese (Brazilian) (pt-br)", 
    "Portuguese (pt)", "Romanian (ro)", "Russian (ru)", "Spanish (es)", "Spanish (Latin American) (es-419)", 
    "Swedish (sv)", "Turkish (tr)", "Welsh (cy)"
]

from pypenguin.helper_functions import pp

projectSchema = {
    "type": "object",
    "properties": {
        "sprites": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
            },
        },
        "globalVariables": {
            "type": "array",
        },
        "globalLists": {
            "type": "array",
        },
        "monitors": {"type": "array"},
        "extensions": {"type": "array"},
        "tempo": {"type": "integer", "minimum": 20, "maximum": 500},
        "videoTransparency": {"type": "number"},
        "videoState": {"type": "string", "enum": ["on", "on flipped", "off"]},
        "textToSpeechLanguage": {
            "type": ["null", "string"],
            "enum": textToSpeechLanguages,
        },
        "extensionData": {"type": "object"},
        "extensionURLs": {"type": "object"},
    },
    "required": [
        "sprites",
        "globalVariables",
        "globalLists",
        "monitors",
        "extensions",
        #"tempo",
        #"videoTransparency",
        #"videoState",
        #"textToSpeechLanguage",
        #"extensionData",
        ###"extensionURLs",
    ],
}

spriteSchema = {
    "type": "object",
    "properties": {
        "isStage": {"type": "boolean", "const": False},
        "name": {"type": "string", "minLength": 1},
        "scripts": {"type": "array"},
        "comments": {"type": "array"},
        "currentCostume": {"type": "integer", "minimum": 0},
        "costumes": {"type": "array"},
        "sounds": {
            "type": "array",
        },
        "volume": {"type": "number", "minimum": 0, "maximum": 100},
        "localVariables": {"type": "array"},
        "localLists": {"type": "array"},
        "layerOrder": {"type": "integer", "minimum": 1},
        "visible": {"type": "boolean"},
        "position": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {"type": "number"},
        "direction": {"type": "number"},
        "draggable": {"type": "boolean"},
        "rotationStyle": {
            "type": "string",
            "enum": ["all around", "left-right", "don't rotate"],
        },
    },
    "required": [
        "isStage",
        "name",
        "scripts",
        "comments",
        "currentCostume",
        "costumes",
        "sounds",
        "volume",
        "layerOrder",
        "visible",
        "position",
        "size",
        "direction",
        "draggable",
        "rotationStyle",
        "localVariables",
        "localLists",
    ],
}

stageSchema = {
    "type": "object",
    "properties": {
        "isStage": {"type": "boolean", "const": True},
        "name": {"type": "string", "const": "Stage"},
        "scripts": {"type": "array"},
        "comments": {"type": "array"},
        "currentCostume": {"type": "integer", "minimum": 0},
        "costumes": {"type": "array"},
        "sounds": {"type": "array"},
        "volume": {"type": "number", "minimum": 0, "maximum": 100},
    },
    "required": [
        "isStage",
        "name",
        "scripts",
        "comments",
        "currentCostume",
        "costumes",
        "sounds",
        "volume",
    ],
}

scriptSchema = {
    "type": "object",
    "properties": {
        "position": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "blocks": {"type": "array", "minItems": 1},
    },
    "required": ["position", "blocks"],
}

costumeSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "extension": {"type": "string"},
        "bitmapResolution": {"type": "integer", "minimum": 1},
        "rotationCenter": {
            "type": "array",
            "items": {"type": ["integer", "number"]},
            "minItems": 2,
            "maxItems": 2,
        },
    },
    "required": [
        "name",
        "extension",
        "bitmapResolution",
        "rotationCenter",
    ],
    "additionalProperties": False,
}

soundSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "extension": {"type": "string"},
        "rate": {"type": "integer", "minimum": 1},
        "sampleCount": {"type": "integer", "minimum": 1},
    },
    "required": ["name", "extension", "rate", "sampleCount"],
}

blockSchema = {
    "type": "object",
    "properties": {
        "opcode": {"type": "string"},
        "inputs": {
            "type": "object",
            "patternProperties": {".+": {"type": "object"}},
            "additionalProperties": False,
        },
        "options": {
            "type": "object",
            "patternProperties": {".+": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
            }},
            "additionalProperties": False,
        },
        "comment": {"type": ["null", "object"]},
    },
    "required": ["opcode", "inputs", "options", "comment"],
}

commentSchema = {
    "type": ["object", "null"],
    "properties": {
        "position": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "isMinimized": {"type": "boolean"},
        "text": {"type": "string"},
    },
    "required": ["position", "size", "isMinimized", "text"],
}

inputSchema = {
    "type": "object",
    "properties": {
        "mode": {
            "type": "string",
            "enum": [
                "block-only",
                "block-and-text",
                "block-and-menu-text",
                "script",
                "block-and-option",
                "block-and-broadcast-option",
            ],
        },
        "block": {"type": ["null", "object"]},
        "text": {"type": "string"},
        "option": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
        },
        "blocks": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["mode"],
}

variableSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "currentValue": {"type": ["string", "number"]},
        "isCloudVariable": {"type": "boolean"},
    },
    "required": ["name", "currentValue"],
}

listSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "currentValue": {
            "type": "array",
            "items": {"type": ["string", "number"]},
        },
    },
    "required": ["name", "currentValue"],
}

monitorSchema = {
    "type": "object",
    "properties": {
        "opcode": {"type": "string", "enum": allowedMenuOpcodes},
        "options": {"type": "object"},
        "spriteName": {"type": ["string", "null"]},
        "size": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "position": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "maxItems": 2,
        },
        "visible": {"type": "boolean"},
        "sliderMin": {"type": "number"},
        "sliderMax": {"type": "number"},
        "onlyIntegers": {"type": "boolean"},
    },
    "required": ["opcode", "options", "spriteName", "position", "visible"],
}

from jsonschema import validate, exceptions


def validateSchema(pathToData, data, schema):
    from pypenguin.helper_functions import pp

    try:
        validate(instance=data, schema=schema)
        error = None
    except exceptions.ValidationError as err:
        # Custom error message
        error_path = list(map(str, pathToData + list(err.absolute_path)))
        error = formatError(ValidationError, error_path, err.message)
    if error != None:
        raise error


def getHelpLink(path):
    def combine(file, section):
        string = f"github.com/Fritzforcode/PyPenguin/blob/main/docs/{file}.md"
        if section != None:
            string += "#" + section
        return string
    if path == []:
        return combine(file="main", section=None)
    primary = path[0]

    if   primary == "sprites":
        isStage = path[1] == 0
        secondary = path[2]
        if   secondary == "isStage"       : pass
        elif secondary == "name"          : pass
        elif secondary == "scripts"       : pass
        elif secondary == "comments"      : pass
        elif secondary == "currentCostume": pass
        elif secondary == "costumes"      : pass
        elif secondary == "sounds"        : pass
        elif secondary == "volume"        : pass
        elif secondary == "layerOrder"    : pass
        elif secondary == "visible"       : pass
        elif secondary == "position"      : pass
        elif secondary == "size"          : pass
        elif secondary == "direction"     : pass
        elif secondary == "draggable"     : pass
        elif secondary == "rotationStyle" : pass
        elif secondary == "localVariables": pass
        elif secondary == "localLists"    : pass
    
    elif primary == "globalVariables":
        pass # Needs completion
    elif primary == "globalLists":
        pass # Needs completion
    elif primary == "tempo":
        pass # Needs completion
    elif primary == "videoTransparency":
        pass # Needs completion
    elif primary == "videoState":
        pass # Needs completion
    elif primary == "textToSpeechLanguage":
        pass # Needs completion
    elif primary == "monitors":
        pass # Needs completion
    elif primary == "extensionData":
        pass # Needs completion
    elif primary == "extensions":
        pass # Needs completion
    elif primary == "extensionURLs":
        pass # Needs completion


def formatError(cls, path, message):
    path = [str(i) for i in path]  # Convert all indexes to string
    if path == []:
        pathString = ""
    else:
        pathString = "at [" + "/".join(path) + "] - "
    link = getHelpLink(path=path)
    return cls(f"{pathString}HELP: {link} - ERROR: {message}")
