from helper_functions import ikv
from validate.constants import validateSchema, formatError, inputSchema, blockSchema, scriptSchema, opcodeDatabase, allowedOpcodes
from validate.comments import validateComment 


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
        newOpcode = block["opcode"]
        for i, oldOpcode, opcodeData in ikv(opcodeDatabase):
            if opcodeData["newOpcode"] == newOpcode:
                break
        if (opcodeData["type"] in ["textReporter"]) and (len(data["blocks"]) > 1):
            raise formatError(path, "A script whose first block is a reporter mustn't have more than one block.")

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
