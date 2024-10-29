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

def validateVariable(path, data, isGlobal):
    # Check variable format
    validateSchema(pathToData=path, data=data, schema=variableSchema)
    validateSchema(pathToData=path+["monitor"], data=data["monitor"], schema=variableMonitorSchema)
    if isGlobal and "isCloudVariable" not in data:
        raise formatError(path=path, message="Global variables must have the 'isCloudVariable' attribute.")
    monitor = data["monitor"]
    if monitor != None:
        if not monitor["sliderMin"] <= monitor["sliderMax"]:
            raise formatError(path=path, message="'sliderMin' must be below 'sliderMax'.")
        if monitor["onlyIntegers"]:
            if not isinstance(monitor["sliderMin"], int):
                raise formatError(path=path+["monitor"]+["sliderMin"], message="Must be an integer because 'onlyIntegers' is true.")
            if not isinstance(monitor["sliderMax"], int):
                raise formatError(path=path+["monitor"]+["sliderMax"], message="Must be an integer because 'onlyIntegers' is true.")
        
def validateList(path, data):
    # Check list format
    validateSchema(pathToData=path, data=data, schema=listSchema)
    validateSchema(pathToData=path+["monitor"], data=data["monitor"], schema=listMonitorSchema)

def validateInputs(path, data, opcode, opcodeData, context):
    allowedInputIDs = list(opcodeData["inputTypes"].keys()) # List of inputs which are defined for the specific opcode
    for i, inputID, inputValue in ikv(data):
        if inputID not in allowedInputIDs:
            raise formatError(path, f"Input '{inputID}' is not defined for a block with opcode '{opcode}'.")
    # Check input formats
    for inputID in allowedInputIDs:
        if inputID not in data:
            raise formatError(path, f"A block with opcode '{opcode}' must have the input '{inputID}'.")

        inputValue = data[inputID]
        # Check input value format
        validateSchema(pathToData=path+[inputID], data=inputValue, schema=inputSchema)
        if inputValue["mode"] == "block-and-text" and "text" not in inputValue: # when the input "text" field is missing
            raise formatError(path+[inputID], f"An input of the 'block-and-text' mode must have the 'text' attribute.")
        if inputValue["block"] != None: # When the input has a block, check the block format
           validateBlock(path=path+[inputID]+["block"], data=inputValue["block"], context=context)
                
        match opcodeData["inputTypes"][inputID]: # type of the input
            case "broadcast":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path+[inputID]+["mode"], f"Must be 'block-and-text' in this case.")
            case "number":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path+[inputID]+["mode"], f"Must be 'block-and-text' in this case.")
                allowedChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
                for char in inputValue["text"]:
                    if char not in allowedChars:
                        raise formatError(path+[inputID], f"The 'text' attribute must be a combination of these characters: {allowedChars}.")
            case "text":
                if inputValue["mode"] != "block-and-text":
                    raise formatError(path+[inputID]+["mode"], f"Must be 'block-and-text' in this case.")

def validateOptions(path, data, opcode, opcodeData, context):
    allowedOptionIDs = list(opcodeData["optionTypes"].keys()) # List of options which are defined for the specific opcode
    for i, optionID, optionValue in ikv(data):
        if optionID not in allowedOptionIDs:
            raise formatError(path, f"Option '{optionID}' is not defined for a block with opcode '{opcode}'.")
    for optionID in allowedOptionIDs:
        if optionID not in data:
            raise formatError(path, f"A block with opcode '{opcode}' must have the option '{optionID}'.")

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
                    raise formatError(path+[optionID], f"Must be one of {possibleValues}.")
            case "broadcast":
                if not isinstance(optionValue, str):
                    raise formatError(path+[optionID], f"Must be a string.")
            case "variable":
                if optionValue not in [var["name"] for var in context["scopeVariables"]]:
                    raise formatError(path+[optionID], f"Must be a defined variable.")
            case "list":
                if optionValue not in [list_["name"] for list_ in context["scopeLists"]]:
                    raise formatError(path+[optionID], f"Must be a defined list.")

def validateComment(path, data):
    validateSchema(pathToData=path, data=data, schema=commentSchema)
    if data != None:
        if data["size"][0] < 52:
            raise formatError(path+["size"]+[0], f"Must be at least 52.")
        if data["size"][1] < 32:
            raise formatError(path+["size"]+[1], f"Must be at least 32.")

def validateBlock(path, data, context):
    # Check block format
    validateSchema(pathToData=path, data=data, schema=blockSchema)

    validateComment(path=path+["comment"], data=data["comment"])
    
    opcode = data["opcode"]
    opcodeData = list(opcodeDatabase.values())[allowedOpcodes.index(opcode)]

    
    validateInputs(
        path=path+["inputs"], 
        data=data["inputs"],
        opcode=opcode, 
        opcodeData=opcodeData,
        context=context, 
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
            raise formatError(path, "'name' of the stage (the first sprite) must always be 'Stage'.")
    else: # If it should be a sprite
        # Check sprite format
        validateSchema(pathToData=path, data=data, schema=spriteSchema)
        
        if data["layerOrder"] < 1:
            raise formatError(path, "'layerOrder' of a sprite must be at least 1.")
        
    # Check script formats
    for j, script in enumerate(data["scripts"]):
        validateScript(path=path+["scripts"]+[j], data=script, context=context)
    
    for j, costume in enumerate(data["costumes"]):
        validateCostume(path=path+["costumes"]+[j], data=costume)
    
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
    

###################################################
# validate costumes, sounds

#ALSO CHECK dataFormat???
#ONLY ALLOW bitmapResolution to be removed when stage and its svg#
#NO OVERLAPPING NAMES IN SOUNDS, COSTUMES, SPRITES?
#ALSO CHECK currentCOSTUME IN RANGE
#validate extension names?
# maybe hide input when in block-only mode? needs research
###################################################

data = readJSONFile("assets/optimized.json")
validateProject(data=data)
print("Validation succeeded")

