import jsonschema
from jsonschema import validate
import jsonschema.exceptions

from helper_functions import readJSONFile, ikv, pp
from validator_constants import opcodeDatabase, projectSchema, allowedOpcodes

###################################################
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
def validateJSONSchema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        return None
    except jsonschema.exceptions.ValidationError as err:
        # Custom error message
        error_path = list(err.absolute_path)
        error_message = f"Validation error at {'/'.join(map(str, error_path))}:\n\t{err.message}"
        return error_message




# following functions detect some errors causes which would not be detected with jsonschema
def validateSprite(i, data):
    if i == 0: # If it should be the stage
        if data["isStage"] != True:
            return "'isStage' of the stage (the first sprite) must always be True"
        if data["name"] != "Stage": 
            return "'name' of the stage (the first sprite) must always be 'Stage'"
    else: # If it should be a sprite
        if data["isStage"] != False:
            return "'isStage' of a non-stage sprite must always be False"
    return None

def validateProject(data):
    for i, sprite in data["sprites"]:
        error = validateSprite(i=i, data=sprite)
        if error: return error

    return None



jsonData = readJSONFile("assets/optimized.json")
error = validateJSONSchema(jsonData, projectSchema)


if not error:
    error = validateProject(data=jsonData)
    if not error:
        print("Valid JSON structure")
    else:
        print(f"Validation failed:\n{error}")
else:
    print(f"Validation failed:\n{error}")

"""
Validation failed:
Validation error at sprites/1/name:
        'Stage' was expected"""
# Why does it force the name to be "Stage" on sprite 1? it shoul only force it upon sprite 0