from helper_functions import readJSONFile, ikv, pp

class ValidationError(Exception):
    pass

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
      #"items"   : { "$ref": "#/definitions/spriteSchema" },
      "minItems": 1
    },
    "variables": {
      "type" : "array",
      #"items": { "$ref": "#/definitions/variableSchema" }
    },
    "lists": {
      "type" : "array",
      #"items": { "$ref": "#/definitions/listSchema" }
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
    "meta"         : { "type": "object" } # Details in metaSchema
  },
  "required": [
    "sprites",
    "variables",
    "lists",
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
    "isStage": { "type": "boolean", "const": False },
    "name"   : { "type": "string" },
    "scripts": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/scriptSchema" }
    },
    "comments": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/commentSchema" }
    },
    "currentCostume": { "type": "integer", "minimum": 0 },
    "costumes": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/costumeSchema" }
    },
    "sounds": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/soundSchema" }
    },
    "volume": {
      "type"   : "number",
      "minimum": 0,
      "maximum": 100
    },
    "layerOrder": { "type": "integer", "minimum": 1 },
    "visible"   : { "type": "boolean" },
    "position"  : {
      "type"    : "array",
      "items"   : { "type": "number" },
      "minItems": 2,
      "maxItems": 2
    },
    "size"         : { "type": "number" },
    "direction"    : { "type": "number" },
    "draggable"    : { "type": "boolean" },
    "rotationStyle": {
      "type": "string",
      "enum": ["all around", "left-right", "don't rotate"]
    }
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
    "rotationStyle"
  ]
}

stageSchema = {
  "type": "object",
  "properties": {
    "isStage": { "type": "boolean", "const": True },
    "name"   : { "type": "string", "const": "Stage" },
    "scripts": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/scriptSchema" }
    },
    "comments": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/commentSchema" }
    },
    "currentCostume": { "type": "integer", "minimum": 0 },
    "costumes": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/costumeSchema" }
    },
    "sounds": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/soundSchema" }
    },
    "volume": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    }
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
    "position": {
      "type"    : "array",
      "items"   : { "type": "integer" },
      "minItems": 2,
      "maxItems": 2
    },
    "blocks": {
      "type" : "array",
#      "items": { "$ref": "#/definitions/blockSchema" }
    }
  },
  "required": ["position", "blocks"]
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
    "options": { "type": "object" },
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
      "maxItems": 2,
      "additionalItems": False
    },
    "minimized": { "type": "boolean" },
    "text"     : { "type": "string" }
  },
  "required": ["position", "size", "minimized", "text"]
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

optionSchema = { "type": "string" }

variableSchema = {
  "type": "object",
  "properties": {
    "name"        : { "type": "string" },
    "currentValue": { "type": ["string", "number"] },
    "mode"        : { "type": "string", "enum": ["cloud", "global", "local"] },
    "sprite"      : { "type": ["string", "null"] },
    "monitor"     : { "$ref": "#/definitions/variableMonitorSchema" }
  },
  "required": ["name", "currentValue", "mode", "sprite", "monitor"]
}

listSchema = {
  "type": "object",
  "properties": {
    "name"        : { "type": "string" },
    "currentValue": {
      "type" : "array",
      "items": ["string", "number"],
    },
    "mode"        : { "type": "string", "enum": ["global", "local"] },
    "sprite"      : { "type": ["string", "null"] },
    "monitor"     : { "$ref": "#/definitions/listMonitorSchema" }
  },
  "required": ["name", "currentValue", "mode", "sprite", "monitor"]
}

variableMonitorSchema = {
  "type": ["object", "null"],
  "properties": {
    "visible": { "type": "boolean" },
    "size"   : {
      "type"    : "array",
      "items"   : { "type": "integer" },
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
      "items"   : { "type": "integer" },
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

metaSchema = {
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

