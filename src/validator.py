import jsonschema
from jsonschema import validate
from helper_functions import readJSONFile, ikv, pp

opcodeDatabase = readJSONFile(filePath="opcode_database.jsonc")
allowedOpcodes = [data["newOpcode"] for data in opcodeDatabase.values()]

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
            "type" : "array",
            "items": [
                # Comments must be at least 52(x) by 32(y) big
                {"type": ["integer", "number"], "minimum": 52},
                {"type": ["integer", "number"], "minimum": 32},
            ],
            "minItems": 2,
            "maxItems": 2,
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
        "name": {"type": "string", "const": "Stage"},
        # common
        "scripts"       : {"type": "array", "items": scriptSchema},
        "comments"      : {"type": "array", "items": commentSchema},
        "currentCostume": {"type": "integer", "minimum":0},
        "costumes"      : {"type": "array", "items": costumeSchema},
        "sounds"        : {"type": "array", "items": soundSchema},
        "volume"        : {"type": ["integer", "number"], "minimum": 0, "maximum": 100},
        "layerOrder"    : {"type": "integer", "minimum": 0}, ! # explore details
        # only stage
        "tempo": {"type": "integer", "minimum": 0}, ! # explore details
        "videoTransparency": {"type": "integer", "minimum": 0, "maximum": 100}, ! # explore details
        "videoState": {"type": "string", "enum": ["on", "", "off"]}, # find middle state; scratch wiki
        "textToSpeechLanguage": {"type": ["null", "string"], "enum": textToSpeechLanguages},
    },        
    "required": ["isStage", "name", "scripts", "comments", "currentCostume", "costumes", "sounds", "volume", "layerOrder", "tempo", "videoTransparency", "videoState", "textToSpeechLanguage"],
}
spriteSchema = {
    "type": "object",
    "properties": {
        # sprite version
        "isStage": {"type": "boolean", "const": False},
        "name": {"type": "string"}, ! #can it be "Stage" too?
        # common
        "scripts"       : stageSchema["properties"]["scripts"],
        "comments"      : stageSchema["properties"]["comments"],
        "currentCostume": stageSchema["properties"]["currentCostume"],
        "costumes"      : stageSchema["properties"]["costumes"],
        "sounds"        : stageSchema["properties"]["sounds"],
        "volume"        : stageSchema["properties"]["volume"],
        "layerOrder"    : stageSchema["properties"]["layerOrder"],
        # sprite only
        "visible": {"type": "boolean"},
        "position": {
            "type": "array",
            "items": {"type": ["integer", "number"]},
            "minItems": 2,
            "maxItems": 2,
        }, ! # check for range maybe
        "size": {"type": ["integer", "number"]}, ! # float too right?
        "direction": {"type": ["integer", "number"]}, ! # float too right?
        "draggable": {"type": "boolean"},
        "rotationStyle": {"type": "string", "enum": ["all around"]}, ! # scratch wiki
    },        
    "required": ["isStage", "name", "scripts", "comments", "currentCostume", "costumes", "sounds", "volume", "layerOrder", "tempo", "videoTransparency", "videoState", "textToSpeechLanguage"],
}
variableSchema = {
    "type": "object",
    "properties": {
        "name"        : {"type": "string"},
        "currentValue": {"type": ["string", "integer", "number"]}, ! # check which types it can be
        "mode"        : {"type": "string", "enum": ["cloud", "global", "local"]},
        "sprite"      : {"type": ["string", "null"]},
    },
    "required": ["name", "currentValue", "mode", "sprite"],
}
listSchema = {
    "type": "object",
    "properties": {
        "name"        : variableSchema["properties"]["name"],
        "currentValue": variableSchema["properties"]["currentValue"],
        "mode"        : {"type": "string", "enum": ["global", "local"]},
        "sprite"      : variableSchema["properties"]["sprite"],
    },
    "required": ["name", "currentValue", "mode", "sprite"],
}
monitorSchema = {
    "type": "object"
}             
projectSchema = {
    "type": "object",
    "properties": {
        "sprites": {
            "type": "array",
            "items"          : stageSchema,
            "additionalItems": spriteSchema,
            "minItems"       : 1,
        },
        "variables"    : {"type": "array", "items": variableSchema},
        "lists"        : {"type": "array", "items": listSchema},
        "monitors"     : {"type": "array", "items": monitorSchema},
        "extensionData": 0,
        "extensions"   : 0,
        "meta"         : 0,
    },
    "required": ["sprites", "variables", "lists", "monitors", "extensionData", "extensions", "meta"],
}

###################################################
#ALSO CHECK BLOCK INPUTS AND OPTIONS WITH A SCRIPT#
#ALSO CHECK currentCOSTUME IN RANGE               #
#ALSO CHECK dataFormat???                         #
#CHECK variable "sprite" existing and fine-ity with local mode
#ONLY ALLOW bitmapResolution to be removed when stage and its svg#
#NO OVERLAPPING NAMES IN SOUNDS, COSTUMES, SPRITES?
###################################################

# Function to validate JSON
def validate_json_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        return True, "JSON is valid"
    except jsonschema.exceptions.ValidationError as err:
        return False, f"Validation error: {err.message}"

def validate_blocks(data):
    for sprite in data["sprites"]:
        for script in sprite["scripts"]:
            for block in script["blocks"]:
                opocdeData = list(opcodeDatabase.values())[allowedOpcodes.index(block["opcode"])]
                pp(opocdeData)
                #for i,inputKey,inputValue in block["inputs"]:
                #    

# Example usage
json_data = readJSONFile("optimized3.json")

is_valid, message = validate_json_schema(json_data, projectSchema)

if is_valid:
    print("Valid JSON structure")
else:
    print(f"Validation failed: {message}")
