import jsonschema
from jsonschema import validate
import jsonschema.exceptions
from helper_functions import readJSONFile, ikv, pp

###################################################
# force stage name
# force isSprite
# force sprite only properties
# force layerOrder: minimum=1 for sprites
# FORCE 52 by 32 on comments
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
        # Custom error message
        error_path = list(err.absolute_path)
        error_message = f"Validation error at {'/'.join(map(str, error_path))}:\n\t{err.message}"
        return False, error_message

# detects some errors which would not be detected with jsonschema
def validate_details(data):
    for sprite in data["sprites"]:
        for script in sprite["scripts"]:
            for block in script["blocks"]:
                opocdeData = list(opcodeDatabase.values())[allowedOpcodes.index(block["opcode"])]
                pp(opocdeData)
                #for i,inputKey,inputValue in block["inputs"]:
                #   
    return True, "JSON is valid"
# Example usage
json_data = readJSONFile("assets/optimized.json")
is_valid, message = validate_json_schema(json_data, projectSchema)


if is_valid:
    is_valid, message = True,7#validate_details(data=json_data)
    if is_valid:
        print("Valid JSON structure")
    else:
        print(f"Validation failed:\n{message}")
else:
    print(f"Validation failed:\n{message}")

"""
Validation failed:
Validation error at sprites/1/name:
        'Stage' was expected"""
# Why does it force the name to be "Stage" on sprite 1? it shoul only force it upon sprite 0