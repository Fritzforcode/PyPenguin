import jsonschema
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
        error = formatError(path=error_path, message=err.message)
    if error != None:
        raise error

def formatError(path, message):
    path = [str(i) for i in path] # Convert all indexes to string
    return ValidationError(f"{('at [' + '/'.join(path) + '] - ') if path != [] else ''}{message}")

#################################################################################################
# the following functions detect some errors causes (which i think can happen)                  #
# which would not be detected with jsonschema                                                   #
# if you find an error cause that is not detected by this this script, tell me on Github        #
#################################################################################################

def validateInputs(path, data, opcode, opcodeData):    
    allowedInputIDs = list(opcodeData["inputTypes"].keys()) # List of inputs which are defined for the specific opcode
    for i, inputID, inputValue in ikv(data):
        if inputID not in allowedInputIDs:
            raise formatError(path, f"Input '{inputID}' is not defined for a block with opcode {opcode}")
    for inputID in allowedInputIDs:
        if inputID not in data:
            raise formatError(path, f"A block with opcode {opcode} must have the input '{inputID}'")

        inputValue = data[inputID]
        match opcodeData["inputTypes"][inputID]: # type of the input
            case "broadcast":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path, f"{inputID} must be in 'block-and-text' mode")
            case "number":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path, f"{inputID} must be in 'block-and-text' mode")
                allowedChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
                for char in inputValue["text"]:
                    if char not in allowedChars:
                        raise formatError(path, f"The 'text' attribute of {inputID} must be a combination of these characters: {allowedChars}")
            case "text":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path, f"{inputID} must be in 'block-and-text' mode")


def validateOptions(path, data, opcode, opcodeData, context):
    allowedOptionIDs = list(opcodeData["optionTypes"].keys()) # List of options which are defined for the specific opcode
    for i, optionID, optionValue in ikv(data):
        if optionID not in allowedOptionIDs:
            raise formatError(path, f"Input '{optionID}' is not defined for a block with opcode {opcode}")
    for optionID in allowedOptionIDs:
        if optionID not in data:
            raise formatError(path, f"A block with opcode {opcode} must have the input '{optionID}'")

        optionValue = data[optionID]
        match opcodeData["optionTypes"][optionID]: # type of the option
            case "key":
                possibleValues = [
                    "space", "up arrow", "down arrow", "right arrow", "left arrow", 
                    "enter", "any", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
                    "x", "y", "z", "-", ",", ".", "`", "=", "[", "]", "\\", ";", "'", 
                    "/", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", 
                    "{", "}", "|", ":", '"', "?", "<", ">", "~", "backspace", "delete", 
                    "shift", "caps lock", "scroll lock", "control", "escape", "insert", 
                    "home", "end", "page up", "page down"
                ]
                if optionValue not in possibleValues:
                    raise formatError(path, f"{optionID} must be one of {possibleValues}")
            case "broadcast":
                if not isinstance(optionValue, str):
                    raise formatError(path, f"{optionID} must be a string")
            case "variable":
                if optionValue not in [var["name"] for var in context["scopeVariables"]]:
                    raise formatError(path, f"{optionID} must be a defined variable")
            case "list":
                if optionValue not in [list_["name"] for list_ in context["scopeLists"]]:
                    raise formatError(path, f"{optionID} must be a defined list")

def validateBlock(path, data, context):
    opcode = data["opcode"]
    opcodeData = list(opcodeDatabase.values())[allowedOpcodes.index(opcode)]
    
    validateInputs(
        path=path+["inputs"], 
        data=data["inputs"], 
        opcode=opcode, 
        opcodeData=opcodeData,
    )
    validateOptions(
        path=path+["options"], 
        data=data["options"], 
        opcode=opcode, 
        opcodeData=opcodeData, 
        context=context,
    )
    

def validateScript(path, data, context):
    for i, block in enumerate(data["blocks"]):
        validateBlock(path=path+["blocks"]+[i], data=block, context=context)

def validateSprite(path, data, context):
    i = path[-1]
    if i == 0: # If it should be the stage
        # Validate stage format
        validateSchema(pathToData=path, data=data, schema=stageSchema)
        if data["name"] != "Stage": 
            raise formatError(path, "'name' of the stage (the first sprite) must always be 'Stage'")
    else: # If it should be a sprite
        # Validate sprite format
        validateSchema(pathToData=path, data=data, schema=spriteSchema)
        
        # Insure the sprite-only properties are given
        for property in ["visible", "position", "size", "direction", "draggable", "rotationStyle"]:
            if property not in data:
                raise formatError(path, f"A non-stage sprite must have the attribute '{property}'")
        
        if data["layerOrder"] < 1:
            raise formatError(path, "'layerOrder' of a non-stage sprite must be at least 1")
        

    for j, script in enumerate(data["scripts"]):
        validateScript(path=path+["scripts"]+[j], data=script, context=context)
    
def validateProject(data):
    # Check project format
    validateSchema(pathToData=[], data=data, schema=projectSchema)
    # Check meta format
    validateSchema(pathToData=["meta"], data=data["meta"], schema=metaSchema)
    
    # Check sprite formats
    for i, sprite in enumerate(data["sprites"]):
        scopeVariables = []
        for variable in data["variables"]:
            if variable["mode"] == "global" \
            or (variable["mode"] == "local" and variable["sprite"] == sprite["name"]): # add global and local variables
                scopeVariables.append(variable)
        scopeLists = []
        for list in data["lists"]:
            if list["mode"] == "global" \
            or (list["mode"] == "local" and list["sprite"] == sprite["name"]): # add global and local lists
                scopeLists.append(list)
        context = {"scopeVariables": scopeVariables, "scopeLists": scopeLists}
        validateSprite(path=["sprites"]+[i], data=sprite, context=context)

###################################################
# force input "text" existing
# FORCE 52 by 32 on comments
#ALSO CHECK BLOCK INPUTS AND OPTIONS WITH A SCRIPT#
# --> check variable or list existance

#ALSO CHECK dataFormat???                         #
#CHECK variable "sprite" existing and fine-ity with local mode
#ONLY ALLOW bitmapResolution to be removed when stage and its svg#
#NO OVERLAPPING NAMES IN SOUNDS, COSTUMES, SPRITES?
#ALSO CHECK currentCOSTUME IN RANGE               #
###################################################

data = readJSONFile("assets/optimized.json")
validateProject(data=data)
print("Validation succeeded")
