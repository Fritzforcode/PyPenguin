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
# the following functions detect some error causes (which i think can happen)                   #
# which can't be detected with jsonschema                                                        #
# if you find an error cause that is not detected by this this script, tell me on Github        #
#################################################################################################

def validateInputs(path, data, context, opcode, opcodeData):
    allowedInputIDs = list(opcodeData["inputTypes"].keys()) # List of inputs which are defined for the specific opcode
    for i, inputID, inputValue in ikv(data):
        if inputID not in allowedInputIDs:
            raise formatError(path, f"Input '{inputID}' is not defined for a block with opcode '{opcode}'")
    # Check input formats
    for inputID in allowedInputIDs:
        if inputID not in data:
            raise formatError(path, f"A block with opcode '{opcode}' must have the input '{inputID}'")

        inputValue = data[inputID]
        # Check input value format
        validateSchema(pathToData=path+[inputID], data=inputValue, schema=inputSchema)
        if inputValue["mode"] == "block-and-text" and "text" not in inputValue: # when the input "text" field is missing
            raise formatError(path+[inputID], f"An input of the 'block-and-text' mode must have the 'text' attribute")
        if inputValue["block"] != None: # When the input has a block, check the block format
           validateBlock(path=path+[inputID]+["block"], data=inputValue["block"], context=context)
                
        match opcodeData["inputTypes"][inputID]: # type of the input
            case "broadcast":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path+[inputID], f"Must be in 'block-and-text' mode")
            case "number":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path+[inputID], f"Must be in 'block-and-text' mode")
                allowedChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
                for char in inputValue["text"]:
                    if char not in allowedChars:
                        raise formatError(path+[inputID], f"The 'text' attribute must be a combination of these characters: {allowedChars}")
            case "text":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path, f"{inputID} must be in 'block-and-text' mode")

def validateOptions(path, data, opcode, opcodeData, context):
    allowedOptionIDs = list(opcodeData["optionTypes"].keys()) # List of options which are defined for the specific opcode
    for i, optionID, optionValue in ikv(data):
        if optionID not in allowedOptionIDs:
            raise formatError(path, f"Option '{optionID}' is not defined for a block with opcode '{opcode}'")
    for optionID in allowedOptionIDs:
        if optionID not in data:
            raise formatError(path, f"A block with opcode '{opcode}' must have the option '{optionID}'")

        optionValue = data[optionID]
        # Check option value format (was paused due to always being a string)
        # validateSchema(pathToData=path+[optionID], data=optionValue, schema=optionSchema)
        
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
                    raise formatError(path+[optionID], f"Must be one of {possibleValues}")
            case "broadcast":
                if not isinstance(optionValue, str):
                    raise formatError(path+[optionID], f"Must be a string")
            case "variable":
                if optionValue not in [var["name"] for var in context["scopeVariables"]]:
                    raise formatError(path+[optionID], f"Must be a defined variable")
            case "list":
                if optionValue not in [list_["name"] for list_ in context["scopeLists"]]:
                    raise formatError(path+[optionID], f"Must be a defined list")

def validateComment(path, data):
    validateSchema(pathToData=path, data=data, schema=commentSchema)
    if data != None:
        if data["size"][0] < 52:
            raise formatError(path+["size"]+[0], f"Must be at least 52")
        if data["size"][1] < 32:
            raise formatError(path+["size"]+[1], f"Must be at least 32")

def validateBlock(path, data, context):
    # Check block format
    validateSchema(pathToData=path, data=data, schema=blockSchema)

    validateComment(path=path+["comment"], data=data["comment"])
    
    opcode = data["opcode"]
    opcodeData = list(opcodeDatabase.values())[allowedOpcodes.index(opcode)]

    
    validateInputs(
        path=path+["inputs"], 
        data=data["inputs"],
        context=context, 
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
    # Check script format
    validateSchema(pathToData=path, data=data, schema=scriptSchema)

    # Check block formats
    for i, block in enumerate(data["blocks"]):
        validateBlock(path=path+["blocks"]+[i], data=block, context=context)

def validateSprite(path, data, context):
    i = path[-1]
    if i == 0: # If it should be the stage
        # Check stage format
        validateSchema(pathToData=path, data=data, schema=stageSchema)
        if data["name"] != "Stage": 
            raise formatError(path, "'name' of the stage (the first sprite) must always be 'Stage'")
    else: # If it should be a sprite
        # Check sprite format
        validateSchema(pathToData=path, data=data, schema=spriteSchema)
        
        # Insure the sprite-only properties are given
        for property in ["visible", "position", "size", "direction", "draggable", "rotationStyle"]:
            if property not in data:
                raise formatError(path, f"A sprite (but not the stage) must have the attribute '{property}'")
        
        if data["layerOrder"] < 1:
            raise formatError(path, "'layerOrder' of a sprite must be at least 1")
        
    # Check script formats
    for j, script in enumerate(data["scripts"]):
        validateScript(path=path+["scripts"]+[j], data=script, context=context)
    
def validateProject(data):
    # Check project format
    validateSchema(pathToData=[], data=data, schema=projectSchema)
    # Check meta format
    validateSchema(pathToData=["meta"], data=data["meta"], schema=metaSchema)
    
    # Check sprite formats
    spriteNames = []
    for i, sprite in enumerate(data["sprites"]):
        scopeVariables = []
        for j, variable in enumerate(data["variables"]):
            validateVariableSchema(path=["variables"]+[j], data=variable)
            if "mode" not in variable:
                raise formatError(path="", message="")
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
        spriteName = None if i == 0 else sprite["name"] # None for the stage
        if spriteName in spriteNames: # If there is the same sprite name twice
            raise formatError(path=["sprites"]+[i]+["name"], message="Sprite names mustn't be the same")
        spriteNames.append(spriteName)
    
    # Check variable formats
    variableNames = {name: [] for name in spriteNames}
    for i, variable in enumerate(data["variables"]):
        validateVariable(path=["variables"]+[i], data=variable, spriteNames=spriteNames)
        variableName = variable["name"]
        spriteName = None if variable["mode"] in ["global", "cloud"] else variable["sprite"] # None for the stage

        error = formatError(path=["variables"]+[i]+["sprite"], message="Variable names mustn't be the same")
        if variable["mode"] in ["global", "cloud"]: 
            # global var: raise if var name alredy exists in any other sprite
            for names in variableNames.values():
                if variableName in names:
                    raise error
        else: 
            # local var: raise if var name alredy exists in own sprite or the stage
            if variableName in (variableNames[None] + variableNames[spriteName]): # If the same variable name alredy exists
                raise error
        variableNames[spriteName].append(variableName) # add it to the vars of its sprite
        
def validateVariableSchema(path, data):
    # Check variable format
    validateSchema(pathToData=path, data=data, schema=variableSchema)
    validateSchema(pathToData=path+["monitor"], data=data["monitor"], schema=variableMonitorSchema)
def validateVariable(path, data, spriteNames):
    if data["sprite"] not in spriteNames:
        raise formatError(path=path+["sprite"], message=f"Sprite '{data['sprite']}' doesn't exist. if you meant to make a stage variable use the 'global' mode and null for sprite")
    if data["mode"] in ["global", "cloud"]: # global var
        if data["sprite"] != None:
            raise formatError(path=path+["sprite"], message="For a non-local variable (see 'mode') this must be null")
    monitor = data["monitor"]
    if monitor != None:
        if not monitor["sliderMin"] <= monitor["sliderMax"]:
            raise formatError(path=path, message="'sliderMin' must be below 'sliderMax'")
        if monitor["onlyIntegers"]:
            if not isinstance(monitor["sliderMin"], int):
                raise formatError(path=path+["monitor"]+["sliderMin"], message="Must be an integer because 'onlyIntegers' is true")
            if not isinstance(monitor["sliderMax"], int):
                raise formatError(path=path+["monitor"]+["sliderMax"], message="Must be an integer because 'onlyIntegers' is true")
        
def validateList(path, data, spriteNames):
    # Check list format
    validateSchema(pathToData=path, data=data, schema=listSchema)
    validateSchema(pathToData=path+["monitor"], data=data["monitor"], schema=listMonitorSchema)
    if data["sprite"] not in spriteNames:
        raise formatError(path=path+["sprite"], message=f"Sprite {data['sprite']} doesn't exist")

###################################################
#validate vars, lists and their monitors
# check var "sprite" being None in global or cloud and sth in local mode


#ALSO CHECK dataFormat???
#ONLY ALLOW bitmapResolution to be removed when stage and its svg#
#NO OVERLAPPING NAMES IN SOUNDS, COSTUMES, SPRITES?
#ALSO CHECK currentCOSTUME IN RANGE
#validate extension names?
###################################################

data = readJSONFile("assets/optimized.json")
validateProject(data=data)
print("Validation succeeded")

# TODO: bring local vars back to sprites again; update validator, optimizer and deoptimizer for that