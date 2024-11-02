from helper_functions import readJSONFile
from validate.errors import ValidationError

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



projectSchema = {
  "type": "object",
  "properties": {
    "sprites": {
      "type"    : "array",
      "minItems": 1
    },
    "globalVariables": {
      "type" : "array",
    },
    "globalLists": {
      "type" : "array",
    },
    "tempo": { "type": "integer", "minimum": 20, "maximum": 500 },
    "videoTransparency": { "type": "number" },
    "videoState": {
      "type": "string",
      "enum": ["on", "on flipped", "off"]
    },
    "textToSpeechLanguage": {
      "type": ["null", "string"],
      "enum": textToSpeechLanguages
    },
    "extensionData": { "type": "object" },
    "extensions"   : { "type": "array"  },
    "meta"         : {
      "type": "object",
      "properties": {
        "semver"  : { "type": "string" },
        "vm"      : { "type": "string" },
        "agent"   : { "type": "string" },
        "platform": {
          "type"      : "object",
          "properties": {
            "name"    : { "type": "string" },
            "url"     : { "type": "string" },
            "version" : { "type": "string" }
          },
        "required": ["name", "url", "version"],
        }
      },
      "required": ["semver", "vm", "agent", "platform"]
    }
  },
  "required": [
    "sprites",
    "globalVariables",
    "globalLists",
    "extensionData",
    "extensions",
    "meta",
    "tempo",
    "videoTransparency",
    "videoState",
    "textToSpeechLanguage"
  ]
}

spriteSchema = {
  "type": "object",
  "properties": {
    "isStage"       : { "type": "boolean", "const": False },
    "name"          : { "type": "string", "minLength": 1 },
    "scripts"       : { "type": "array" },
    "comments"      : { "type": "array" },
    "currentCostume": { "type": "integer", "minimum": 0 },
    "costumes"      : { "type": "array" },
    "sounds"        : { "type": "array", },
    "volume"        : { "type": "number", "minimum": 0, "maximum": 100 },
    "localVariables": { "type": "array" },
    "localLists"    : { "type": "array" },
    "layerOrder"    : { "type": "integer", "minimum": 1 },
    "visible"       : { "type": "boolean" },
    "position"      : { "type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2 },
    "size"          : { "type": "number" },
    "direction"     : { "type": "number" },
    "draggable"     : { "type": "boolean" },
    "rotationStyle" : { "type": "string", "enum": ["all around", "left-right", "don't rotate"]}
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
    "localLists"
  ]
}

stageSchema = {
  "type": "object",
  "properties": {
    "isStage"       : { "type": "boolean", "const": True },
    "name"          : { "type": "string", "const": "Stage" },
    "scripts"       : { "type": "array" },
    "comments"      : { "type": "array" },
    "currentCostume": { "type": "integer", "minimum": 0 },
    "costumes"      : { "type": "array" },
    "sounds"        : { "type": "array" },
    "volume"        : { "type": "number", "minimum": 0, "maximum": 100 }
  },
  "required": [
    "isStage",
    "name",
    "scripts",
    "comments",
    "currentCostume",
    "costumes",
    "sounds",
    "volume"
  ]
}

scriptSchema = {
  "type": "object",
  "properties": {
    "position": { "type": "array", "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
    "blocks"  : { "type" : "array", "minItems": 1 }
  },
  "required": ["position", "blocks"]
}

costumeSchema = {
  "type": "object",
  "properties": {
    "name"            : { "type": "string" },
    "dataFormat"      : { "type": "string" },
    "fileStem"        : { "type": "string" },
    "bitmapResolution": { "type": "integer", "minimum": 1 },
    "rotationCenter": {
      "type": "array",
      "items": { "type": ["integer", "number"] },
      "minItems": 2,
      "maxItems": 2
    }
  },
  "required": ["name", "dataFormat", "fileStem", "bitmapResolution", "rotationCenter"]
}

soundSchema = {
  "type": "object",
  "properties": {
    "name"       : { "type": "string" },
    "dataFormat" : { "type": "string" },
    "fileStem"   : { "type": "string" },
    "rate"       : { "type": "integer", "minimum": 1 },
    "sampleCount": { "type": "integer", "minimum": 1 }
  },
  "required": ["name", "dataFormat", "fileStem", "rate", "sampleCount"]
}

blockSchema = {
  "type": "object",
  "properties": {
    "opcode": {
      "type": "string",
      "enum": allowedOpcodes
    },
    "inputs": {
      "type": "object",
      "patternProperties": {
        "^[a-zA-Z0-9_]+$": { "type": "object" }
      },
      "additionalProperties": False
    },
    "options": { 
      "type": "object",
      "patternProperties": {
        "^[a-zA-Z0-9_]+$": { "type": "string" }
      },
      "additionalProperties": False
    },
    "comment": { "type": ["null", "object"] }
  },
  "required": ["opcode", "inputs", "options", "comment"]
}

commentSchema = {
  "type": ["object", "null"],
  "properties": {
    "position": {
      "type"    : "array",
      "items"   : { "type": "number" },
      "minItems": 2,
      "maxItems": 2
    },
    "size": {
      "type"    : "array",
      "items"   : { "type": "number" },
      "minItems": 2,
      "maxItems": 2
    },
    "isMinimized": { "type": "boolean" },
    "text"       : { "type": "string" }
  },
  "required": ["position", "size", "isMinimized", "text"]
}

inputSchema = {
  "type": "object",
  "properties": {
    "mode": { "type": "string", "enum": ["block-only", "block-and-text"] },
    "block": { "type": ["null", "object"] },
    "text": { "type": "string" }
  },
  "required": ["mode", "block"]
}

variableSchema = {
  "type": "object",
  "properties": {
    "name"           : { "type": "string", "minLength": 1 },
    "currentValue"   : { "type": ["string", "number"] },
    "monitor"        : { "type": ["object", "null"] },
    "isCloudVariable": { "type": "boolean" }
  },
  "required": ["name", "currentValue", "monitor"]
}

listSchema = {
  "type": "object",
  "properties": {
    "name"        : { "type": "string", "minLength": 1 },
    "currentValue": { "type" : "array", "items": {"type": ["string", "number"]} },
    "monitor"     : { "type": ["object", "null"] }
  },
  "required": ["name", "currentValue", "monitor"]
}

variableMonitorSchema = {
  "type": ["object", "null"],
  "properties": {
    "visible": { "type": "boolean" },
    "size"   : {
      "type"    : "array",
      "items"   : { "type": "integer", "minimum": 0 },
      "minItems": 2,
      "maxItems": 2
    },
    "position": {
      "type"    : "array",
      "items"   : { "type": "integer" },
      "minItems": 2,
      "maxItems": 2
    },
    "sliderMin"   : { "type": "number" },
    "sliderMax"   : { "type": "number" },
    "onlyIntegers": { "type": "boolean" }
  },
  "required": ["visible", "size", "position", "sliderMin", "sliderMax", "onlyIntegers"]
  }

listMonitorSchema = {
  "type": ["object", "null"],
  "properties": {
    "visible": { "type": "boolean" },
    "size": {
      "type"    : "array",
      "items"   : { "type": "integer", "minimum": 0 },
      "minItems": 2,
      "maxItems": 2
    },
    "position": {
      "type"    : "array",
      "items"   : { "type": "integer" },
      "minItems": 2,
      "maxItems": 2
    }
  },
  "required": ["visible", "size", "position"]
}

from jsonschema import validate, exceptions

def validateSchema(pathToData, data, schema):
    
    try:
        validate(instance=data, schema=schema)
        error = None
    except exceptions.ValidationError as err:
        # Custom error message
        error_path = list(map(str, pathToData + list(err.absolute_path)))
        error = formatError(path=error_path, message=err.message)
    if error != None:
        raise error


def formatError(path, message):
    path = [str(i) for i in path] # Convert all indexes to string
    return ValidationError(f"{('at [' + '/'.join(path) + '] - ') if path != [] else ''}{message}")

