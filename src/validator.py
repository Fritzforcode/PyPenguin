import jsonschema
from jsonschema import validate
from helper_functions import readJSONFile, ikv, pp

opcodeDatabase = readJSONFile(filePath="opcode_database.jsonc")
allowedOpcodes = [data["newOpcode"] for data in opcodeDatabase.values()]

commentSchema = {
    "type": ["object", "null"],
    "properties": {
        "position": {
            "type": "array",
            "items": {"type": ["number", "integer"]},
            "minItems": 2,
            "maxItems": 2,
        },
        "size": {
            "type": "array",
            "items": [
                # Comments must be at least 52(x) by 32(y) big
                {"type": ["integer", "number"], "minimum": 52},
                {"type": ["integer", "number"], "minimum": 32},
            ],
            "minItems": 2,
            "maxItems": 2,
        },
        "minimized": {"type": "boolean"},
        "text": {"type": "string"},
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
            "position": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 2,
                "maxItems": 2,
            },
            "blocks": {"type": "array", "items": blockSchema},
        },
        "required": ["position", "blocks"],
}
"""            {
        "position": [301, 258],
        "blocks": [
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": null,
                        "text": "0"
                    }
                },
                "options": {
                    "VARIABLE": "my variable"
                },
                "comment": null
            },
            {
                "opcode": "change [VARIABLE] by (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": null,
                        "text": "1"
                    }
                },
                "options": {
                    "VARIABLE": "d"
                },
                "comment": null
            },
            {
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": null,
                        "text": "0"
                    }
                },
                "options": {
                    "VARIABLE": "ydx"
                },
                "comment": null
            },
            {
                "opcode": "change [VARIABLE] by (VALUE)",
                "inputs": {
                    "VALUE": {
                        "mode": "block-and-text",
                        "block": null,
                        "text": "1"
                    }
                },
                "options": {
                    "VARIABLE": "zt"
                },
                "comment": null
            },
            {
                "opcode": "add (ITEM) to [LIST]",
                "inputs": {
                    "ITEM": {
                        "mode": "block-and-text",
                        "block": null,
                        "text": "thing"
                    }
                },
                "options": {
                    "LIST": "add"
                },
                "comment": null
            }
        ]
    }"""
costumeSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "bitmapResolution": {"type": "integer", "minimum": 1},
        "dataFormat": {"type": "string"},
        "fileStem": {"type": "string"},
        "rotationCenter": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {"type": ["integer", "number"]},
        },
    },
    "required": ["name", "dataFormat", "fileStem", "rotationCenter"],

}
soundSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "dataFormat": {"type": "string"},
        "fileStem": {"type": "string"},
        "rate": {"type": "integer"},
        "sampleCount": {"type": "integer"},
    },
    "required": [],
}
stageSchema = {

    "type": "object",
    "properties": {
        "isStage": {"type": "boolean", "const": True},
        "name": {"type": "string", "const": "Stage"},
        "scripts": {"type": "array", "items": scriptSchema},
        "comments": {"type": "array", "items": commentSchema},
        "currentCostume": {"type": "integer", "minimum":0},
        "costumes": {"type": "array", "items": costumeSchema},
        "sounds": {"type": "array", "items": soundSchema},
        #"sounds": [],
        #"volume": 100,
        #"layerOrder": 0,
        #"tempo": 60,
        #"videoTransparency": 50,
        #"videoState": "on",
        #"textToSpeechLanguage": None,
        "required": ["isStage", "name", "scripts", "comments", "currentCostume", "costumes", "sounds", "volume", "layerOrder", "tempo", "videoTransparency", "videoState", "textToSpeechLanguage"],
    },
}
spriteSchema = {}
projectSchema = {
    "type": "object",
    "properties": {
        "sprites": {
            "type": "array",
            "items": stageSchema,
            "additionalItems": spriteSchema,
            "minItems": 1,
        },
        "variables": 0,
        "lists": 0,
        "monitors": 0,
        "extensionData": 0,
        "extensions": 0,
        "meta": 0,
    },
    "required": ["sprites", "variables", "lists", "monitors", "extensionData", "extensions", "meta"],
}

###################################################
#ALSO CHECK BLOCK INPUTS AND OPTIONS WITH A SCRIPT#
#ALSO CHECK currentCOSTUME IN RANGE               #
#ALSO CHECK dataFormat???                         #
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
