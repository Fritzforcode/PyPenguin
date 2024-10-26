from jsonschema import validate, exceptions

from helper_functions import readJSONFile, ikv, pp
from validator_constants import *



def validateSchema(pathToData, data, schema):
    try:
        validate(instance=data, schema=schema)
        error = None
    except exceptions.ValidationError as err:
        # Custom error message
        error_path = list(map(str, pathToData + list(err.absolute_path)))
        error = ValidationError(f"{('at [' + '/'.join(error_path) + '] - ') if error_path != [] else ''}{err.message}")
    if error != None:
        raise error

def validateInputs(path, data):
    pass

def validateOptions(path, data):
    pass
        
def validateBlock(path, data):
    pass
        
def validateScript(path, data):
    # Check block formats
    for i, block in enumerate(data["blocks"]):
        validateBlock(path=path+["blocks"]+[i], data=block)

def validateSprite(path, data):
    # Check script formats
    for i, script in enumerate(data["scripts"]):
        validateScript(path=path+["scripts"]+[i], data=script)

def validateProject(data):
    # Check project format
    validateSchema(pathToData=[], data=data, schema=projectSchema)
    # Check meta format
    validateSchema(pathToData=["meta"], data=data["meta"], schema=metaSchema)
    # Check sprite formats
    for i, sprite in enumerate(data["sprites"]):
        validateSprite(path=["sprites"]+[i], data=sprite)

validateProject(
    data = readJSONFile("assets/optimized.json")
)

print("Validation Succeeded")
