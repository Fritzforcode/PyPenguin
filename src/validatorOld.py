import jsonschema
from jsonschema import validate

variablesSchema = {
    "type": "object",
    "patternProperties": {
        "^.*$": { # Any string can be key
            "type": "array",
            we
        },
    },
    "additionalProperties": False, # Disallow any non-String keys
}
stageSchema = {
    "type": "object",
    "properties": {
        
    },
}
spriteSchema = {
    "type": "object",
    "properties": {
        "isStage": {"type": "boolean"},
        "name": {"type": "string", "const":"Stage"},
        "variables": variablesSchema,
        #"variables": {
        #    "`jEk@4|i[#Fk?(8x)AV.-my variable": [
        #        "my variable",
        #        0
        #    ]
        #},
        #"lists": {},
        #"broadcasts": {},
        #"customVars": [],
        #"blocks": {},
        #"comments": {},
        #"currentCostume": 0,
        #"costumes": [
        #    {
        #        "name": "backdrop1",
        #        "dataFormat": "svg",
        #        "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
        #        "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
        #        "rotationCenterX": 240,
        #        "rotationCenterY": 180
        #    }
        #],
        #"sounds": [],
        #"id": "p]_uD8#0^Q=ryfqeQLud",
        #"volume": 100,
        #"layerOrder": 0,
        #"tempo": 60,
        #"videoTransparency": 50,
        #"videoState": "on",
        #"textToSpeechLanguage": null
    },
}
projectSchema = {
    "type": "object",
    "properties": {
        "targets": {
            "type": "array",
            "items": stageSchema,
            "additionalItems": spriteSchema,
            "minItems": 1,
        },
    },
    "required": ["name", "age"]
}

# Function to validate JSON
def validate_json_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        return True, "JSON is valid"
    except jsonschema.exceptions.ValidationError as err:
        return False, f"Validation error: {err.message}"

# Example usage
json_data = {
    "name": "John",
    "age": 30
}

is_valid, message = validate_json_schema(json_data, schema)

if is_valid:
    print("Valid JSON structure")
else:
    print(f"Validation failed: {message}")
