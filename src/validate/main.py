from validate.constants import validateSchema, formatError, projectSchema, metaSchema
from validate.variables_lists import validateVariable, validateList
from validate.sprites import validateSprite

def validateProject(data):
    # Check project format
    validateSchema(pathToData=[], data=data, schema=projectSchema)
    # Check meta format
    validateSchema(pathToData=["meta"], data=data["meta"], schema=metaSchema)
    
    # Check variable formats
    errorMessage = "Variable names mustn't be the same. Please check 'globalVariables' and 'localVariables' of the same sprite."
    globalVariableNames = []
    for j, variable in enumerate(data["globalVariables"]):
        validateVariable(path=["globalVariables"]+[j], data=variable, isGlobal=True)
        variableName = variable["name"]
        if variableName in globalVariableNames: # if var name alredy exists globally
            raise formatError(path=["globalVariables"]+[j]+["name"], message=errorMessage)
    
    localVariableNames = [[] for i in range(  len( data["sprites"][1:] )  )]
    for i, sprite in enumerate(data["sprites"][1:]):
        if "localVariables" not in sprite:
            raise formatError(path=["sprites"]+[i], message="Each sprite (but not the stage) must have the 'localVariables' attribute.")
        if not isinstance(sprite["localVariables"], list):
            raise formatError(path=["sprites"]+[i]+["localVariables"], message="Must be an array.")
        
        for j, variable in enumerate(sprite["localVariables"]):
            validateVariable(path=["sprites"]+[i]+["localVariables"]+[j], data=variable, isGlobal=False)
            variableName = variable["name"]
            if variableName in globalVariableNames or variableName in localVariableNames[i]: # if var name alredy exists globally or in the same sprite
                raise formatError(path=["sprites"]+[i]+["localVariables"]+[j]+["name"], message=errorMessage)
    
    
    errorMessage = "List names mustn't be the same. Please check 'globalLists' and 'localLists' of the same sprite."
    globalListNames = []
    for j, list_ in enumerate(data["globalLists"]):
        validateList(path=["globalLists"]+[j], data=list_)
        listName = list_["name"]
        if listName in globalListNames: # if list name alredy exists globally
            raise formatError(path=["globalLists"]+[j]+["name"], message=errorMessage)
    
    localListNames = [[] for i in range(  len( data["sprites"][1:] )  )]
    for i, sprite in enumerate(data["sprites"][1:]):
        if "localLists" not in sprite:
            raise formatError(path=["sprites"]+[i], message="Each sprite (but not the stage) must have the 'localLists' attribute.")
        if not isinstance(sprite["localLists"], list):
            raise formatError(path=["sprites"]+[i]+["localLists"], message="Must be an array.")
        
        for j, list_ in enumerate(sprite["localLists"]):
            validateList(path=["sprites"]+[i]+["localLists"]+[j], data=list_)
            listName = list_["name"]
            if listName in globalListNames or listName in localListNames[i]: # if list name alredy exists globally or in the same sprite
                raise formatError(path=["sprites"]+[i]+["localLists"]+[j]+["name"], message=errorMessage)
    

    # Check sprite formats
    spriteNames = []
    for i, sprite in enumerate(data["sprites"]):
        if i == 0:
            scopeVariables = data["globalVariables"]
            scopeLists     = data["globalLists"]
        else:
            scopeVariables = sprite["localVariables"] + data["globalVariables"]
            scopeLists     = sprite["localLists"]     + data["globalLists"]
        
        context = {"scopeVariables": scopeVariables, "scopeLists": scopeLists}
        validateSprite(path=["sprites"]+[i], data=sprite, context=context)
        spriteName = None if i == 0 else sprite["name"] # None for the stage
        if spriteName in spriteNames: # If there is the same sprite name twice
            raise formatError(path=["sprites"]+[i]+["name"], message="Sprite names mustn't be the same.")
        spriteNames.append(spriteName)
    

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
    "meta"         : { "type": "object" } # Details in metaSchema
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
}

soundSchema = {
  "type": "object",
  "properties": {
    "name"       : { "type": "string" },
    "dataFormat" : { "type": "string" },
    "fileStem"   : { "type": "string" },
    "rate"       : { "type": "integer", "minimum": 0 },
    "sampleCount": { "type": "integer", "minimum": 0 }
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
    "name"        : { "type": "string" },
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
