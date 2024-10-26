import jsonschema
from jsonschema import validate as validate
import jsonschema.exceptions

from helper_functions import readJSONFile, ikv, pp
from validator_constants import opcodeDatabase, schema, allowedOpcodes

def formatError(path, message):
    path = [str(i) for i in path] # Convert all indexes to string
    return f"Validation error at {'/'.join(path)}:\n\t{message}"



#################################################################################################
# the following functions detect some errors causes (which i think can happen)                  #
# which would not be detected with jsonschema                                                   #
# if you find an error cause that is not detected by this this script, tell me on Github        #
#################################################################################################

def validateInputs(path, data, opcode, opcodeData):
    allowedInputIDs = list(opcodeData["inputTypes"].keys()) # List of inputs which are defined for the specific opcode
    for i, inputID, inputValue in ikv(data):
        if inputID not in allowedInputIDs:
            return formatError(path, f"Input '{inputID}' is not defined for a block with opcode {opcode}")
    for inputID in allowedInputIDs:
        if inputID not in data:
            return formatError(path, f"A block with opcode {opcode} must have the input '{inputID}'")

        inputValue = data[inputID]
        match opcodeData["inputTypes"][inputID]: # type of the input
            case "broadcast":
                if inputValue["mode"] != "block-and-text":
                    return formatError(path, f"{inputID} must be in 'block-and-text' mode")
            case "number":
                if inputValue["mode"] != "block-and-text":
                    return formatError(path, f"{inputID} must be in 'block-and-text' mode")
                allowedChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
                for char in inputValue["text"]:
                    if char not in allowedChars:
                        return formatError(path, f"The 'text' attribute of {inputID} must be a combination of these characters: {allowedChars}")
            case "text":
                if inputValue["mode"] != "block-and-text":
                    return formatError(path, f"{inputID} must be in 'block-and-text' mode")
    return None # else no error


def validateOptions(path, data, opcode, opcodeData, context):
    allowedOptionIDs = list(opcodeData["optionTypes"].keys()) # List of options which are defined for the specific opcode
    for i, optionID, optionValue in ikv(data):
        if optionID not in allowedOptionIDs:
            return formatError(path, f"Input '{optionID}' is not defined for a block with opcode {opcode}")
    for optionID in allowedOptionIDs:
        if optionID not in data:
            return formatError(path, f"A block with opcode {opcode} must have the input '{optionID}'")

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
                    return formatError(path, f"{optionID} must be one of {possibleValues}")
            case "broadcast":
                if not isinstance(optionValue, str):
                    return formatError(path, f"{optionID} must be a string")
            case "variable":
                if optionValue not in [var["name"] for var in context["scopeVariables"]]:
                    return formatError(path, f"{optionID} must be a defined variable")
            case "list":
                if optionValue not in [list_["name"] for list_ in context["scopeLists"]]:
                    return formatError(path, f"{optionID} must be a defined list")
    return None #else no error

def validateBlock(path, data, context):
    opcode = data["opcode"]
    opcodeData = list(opcodeDatabase.values())[allowedOpcodes.index(opcode)]
    
    error = validateInputs(
        path=path+["inputs"], 
        data=data["inputs"], 
        opcode=opcode, 
        opcodeData=opcodeData,
    )
    if error: return error
    error = validateOptions(
        path=path+["options"], 
        data=data["options"], 
        opcode=opcode, 
        opcodeData=opcodeData, 
        context=context,
    )
    if error: return error
    


    return None # else no error

def validateScript(path, data, context):
    for i, block in enumerate(data["blocks"]):
        error = validateBlock(path=path+["blocks"]+[i], data=block, context=context)
        if error: return error
    return None # else no error

def validateSprite(path, data, context):
    i = path[-1]
    if i == 0: # If it should be the stage
        if data["isStage"] != True:
            return formatError(path, "'isStage' of the stage (the first sprite) must always be True")
        if data["name"] != "Stage": 
            return formatError(path, "'name' of the stage (the first sprite) must always be 'Stage'")
    else: # If it should be a sprite
        if data["isStage"] != False:
            return formatError(path, "'isStage' of a non-stage sprite must always be False")
        
        # Insure the sprite-only properties are given
        for property in ["visible", "position", "size", "direction", "draggable", "rotationStyle"]:
            if property not in data:
                return formatError(path, f"A non-stage sprite must have the attribute '{property}'")
        
        if data["layerOrder"] < 1:
            return formatError(path, "'layerOrder' of a non-stage sprite must be at least 1")
        

    for j, script in enumerate(data["scripts"]):
        error = validateScript(path=path+["scripts"]+[j], data=script, context=context)
        if error: return error
    return None # else no error

def validateProject(data):
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
        error = validateSprite(path=["sprites"]+[i], data=sprite, context=context)
        if error: return error

    return None # else no error

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

jsonData = readJSONFile("assets/optimized.json")
error = validateJSONSchema(jsonData=jsonData, schema=schema)


#if not error:
#    error = validateProject(data=jsonData)
#    if not error:
#        print("Validation succeeded")
#    else:
#        indentedError = "\t" + "\n\t".join(error.splitlines())
#        print(f"Validation failed:\n{indentedError}")
#else:
#    indentedError = "\t" + "\n\t".join(error.splitlines())
#    print(f"Validation failed:\n{indentedError}")

