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

schema = {
  "definitions": {
    "commentSchema": {
      "type": ["object", "null"],
      "properties": {
        "position": {
          "type"    : "array",
          "items"   : { "type": ["number", "integer"] },
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
    },
    "blockSchema": {
      "type": "object",
      "properties": {
        "opcode": {
          "type": "string",
          "enum": allowedOpcodes
        },
        "inputs": {
          "type": "object",
          "patternProperties": {
            "^[a-zA-Z0-9_]+$": { "$ref": "#/definitions/inputSchema" }
          },
          "additionalProperties": False
        },
        "options": { "type": "object" },
        "comment": { "$ref": "#/definitions/commentSchema" }
      },
      "required": ["opcode", "inputs", "options", "comment"]
    },
    "inputSchema": {
      "oneOf": [
        {
          "type": "object",
          "properties": {
            "mode": { "type": "string", "const": "block-only" },
            "block": {
              "oneOf": [
                { "type": "null" },
                { "$ref": "#/definitions/blockSchema" }
              ]
            }
          }
        }
      ]
    },
    "scriptSchema": {
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
          "items": { "$ref": "#/definitions/blockSchema" }
        }
      },
      "required": ["position", "blocks"]
    },
    "costumeSchema": {
      "type": "object",
      "properties": {
        "name"            : { "type": "string" },
        "bitmapResolution": { "type": "integer", "minimum": 1 },
        "dataFormat"      : { "type": "string" },
        "fileStem"        : { "type": "string" },
        "rotationCenter": {
          "type": "array",
          "items": { "type": ["integer", "number"] },
          "minItems": 2,
          "maxItems": 2
        }
      },
      "required": ["name", "dataFormat", "fileStem", "rotationCenter"]
    },
    "soundSchema": {
      "type": "object",
      "properties": {
        "name"       : { "type": "string" },
        "dataFormat" : { "type": "string" },
        "fileStem"   : { "type": "string" },
        "rate"       : { "type": "integer" },
        "sampleCount": { "type": "integer" }
      },
      "required": ["name", "dataFormat", "fileStem", "rate", "sampleCount"]
    },
    "stageSchema": {
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
    },
    "spriteSchema": {
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
        "layerOrder": { "type": "integer", "minimum": 0 },
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
        "layerOrder"
      ]
    },
    "variableMonitorSchema": {
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
        "sliderMin"   : { "type": ["integer", "number"] },
        "sliderMax"   : { "type": ["integer", "number"] },
        "onlyIntegers": { "type": "boolean" }
      },
      "required": ["visible", "size", "position", "sliderMin", "sliderMax", "onlyIntegers"]
    },
    "variableSchema": {
      "type": "object",
      "properties": {
        "name"        : { "type": "string" },
        "currentValue": { "type": ["string", "integer", "number"] },
        "mode"        : { "type": "string", "enum": ["cloud", "global", "local"] },
        "sprite"      : { "type": ["string", "null"] },
        "monitor"     : { "$ref": "#/definitions/variableMonitorSchema" }
      },
      "required": ["name", "currentValue", "mode", "sprite", "monitor"]
    },
    "listMonitorSchema": {
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
    },
    "listSchema": {
      "type": "object",
      "properties": {
        "name": { "$ref": "#/definitions/variableSchema/properties/name" },
        "currentValue": {
          "type" : "array",
          "items": { "$ref": "#/definitions/variableSchema/properties/currentValue" }
        },
        "mode"   : { "type": "string", "enum": ["global", "local"] },
        "sprite" : { "$ref": "#/definitions/variableSchema/properties/sprite" },
        "monitor": { "$ref": "#/definitions/listMonitorSchema" }
      },
      "required": ["name", "currentValue", "mode", "sprite", "monitor"]
    },
    "metaSchema": {
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
          }
        }
      }
    }
  },
  "projectSchema": {
    "type": "object",
    "properties": {
      "sprites": {
        "type"    : "array",
        "items"   : { "$ref": "#/definitions/spriteSchema" },
        "minItems": 1
      },
      "variables": {
        "type" : "array",
        "items": { "$ref": "#/definitions/variableSchema" }
      },
      "lists": {
        "type" : "array",
        "items": { "$ref": "#/definitions/listSchema" }
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
      "extensions"   : { "type": "array" },
      "meta"         : { "$ref": "#/definitions/metaSchema" }
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
}
