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
    "videoTransparency": { "type": ["integer", "number"] },
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
    "isStage": { "type": "boolean" },
    "name"   : { "type": "string" },
    "scripts": {
      "type" : "array",
      "items": { "$ref": "#/definitions/scriptSchema" }
    },
    "comments": {
      "type" : "array",
      "items": { "$ref": "#/definitions/commentSchema" }
    },
    "currentCostume": { "type": "integer", "minimum": 0 },
    "costumes": {
      "type" : "array",
      "items": { "$ref": "#/definitions/costumeSchema" }
    },
    "sounds": {
      "type" : "array",
      "items": { "$ref": "#/definitions/soundSchema" }
    },
    "volume": {
      "type"   : ["integer", "number"],
      "minimum": 0,
      "maximum": 100
    },
    "layerOrder": { "type": "integer", "minimum": 1 },
    "visible"   : { "type": "boolean" },
    "position"  : {
      "type"    : "array",
      "items"   : { "type": ["integer", "number"] },
      "minItems": 2,
      "maxItems": 2
    },
    "size"         : { "type": ["integer", "number"] },
    "direction"    : { "type": ["integer", "number"] },
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
      "items": { "$ref": "#/definitions/scriptSchema" }
    },
    "comments": {
      "type" : "array",
      "items": { "$ref": "#/definitions/commentSchema" }
    },
    "currentCostume": { "type": "integer", "minimum": 0 },
    "costumes": {
      "type" : "array",
      "items": { "$ref": "#/definitions/costumeSchema" }
    },
    "sounds": {
      "type" : "array",
      "items": { "$ref": "#/definitions/soundSchema" }
    },
    "volume": {
      "type": ["integer", "number"],
      "minimum": 0,
      "maximum": 100
    },
    "layerOrder": { "type": "integer", "const": 0 }
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
    "layerOrder"
  ]
}

variableSchema = {}

listSchema = {}

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


