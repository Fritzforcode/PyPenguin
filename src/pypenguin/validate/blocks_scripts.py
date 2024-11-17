from pypenguin.helper_functions import ikv, parseCustomOpcode
from pypenguin.validate.constants import validateSchema, formatError, inputSchema, blockSchema, scriptSchema, opcodeDatabase, allowedOpcodes
from pypenguin.validate.comments import validateComment
from pypenguin.database import inputDefault, optionDefault, commentDefault, inputModes, inputBlockDefault, inputTextDefault, inputBlocksDefault


def validateBlock(path, data, context):
    if "inputs" not in data:
        data["inputs"] = inputDefault
    if "options" not in data:
        data["options"] = optionDefault
    if "comment" not in data:
        data["comment"] = commentDefault
    
    # Check block format
    validateSchema(pathToData=path, data=data, schema=blockSchema)

    validateComment(path=path+["comment"], data=data["comment"])
    
    opcode = data["opcode"]
    opcodeData = list(opcodeDatabase.values())[allowedOpcodes.index(opcode)]
    

    validateOptions(
        path=path+["options"], 
        data=data["options"], 
        opcode=opcode, 
        opcodeData=opcodeData, 
        context=context,
    )
    validateInputs(
        path=path+["inputs"], 
        data=data["inputs"],
        opcode=opcode, 
        opcodeData=opcodeData,
        context=context, 
        optionDatas=data["options"],
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
        if (opcodeData["type"] in ["stringReporter", "numberReporter", "booleanReporter"]) and (len(data["blocks"]) > 1):
            raise formatError(path, "A script whose first block is a reporter mustn't have more than one block.")

def validateInputs(path, data, opcode, opcodeData, context, optionDatas):
    allowedInputIDs = list(opcodeData["inputTypes"].keys()) # List of inputs which are defined for the specific opcode
    if opcode == "call ...": # Inputs in the call block type are custom
        proccode, inputTypes = parseCustomOpcode(optionDatas["customOpcode"])
        inputTypes = {k: ("text" if v==str else "boolean") for i,k,v in ikv(inputTypes)}
        for i, inputID, inputType in ikv(inputTypes):
            if inputType == "text" and inputID not in data:
                raise formatError(path, f"A custom block with custom opcode '{optionDatas['customOpcode']}' must have the input '{inputID}'.")
    else:
        inputTypes = opcodeData["inputTypes"]
        for i, inputID, inputValue in ikv(data):
            if inputID not in allowedInputIDs:
                raise formatError(path, f"Input '{inputID}' is not defined for a block with opcode '{opcode}'.")
        for inputID in allowedInputIDs:
            inputType = inputTypes[inputID]
            if inputType not in ["boolean", "round", "script"]:
                if inputID not in data:
                    raise formatError(path, f"A block with opcode '{opcode}' must have the input '{inputID}'.")
    # Check input formats
    for inputID in data:
        if opcode == "call ...":
            if inputID not in inputTypes:
                raise formatError(path, f"Input '{inputID}' is not defined for a custom block with custom opcode '{optionDatas['customOpcode']}'.")
        inputType = inputTypes[inputID]

        if inputID in data:
            inputMode = inputModes[inputType]

            inputValue = data[inputID]
            if "mode" not in inputValue:
                inputValue["mode"] = inputMode
            # Check input value format
            validateSchema(pathToData=path+[inputID], data=inputValue, schema=inputSchema)
            if   inputMode == "block-and-text":
                required = ["block", "text"]
            elif inputMode == "block-only":
                required = ["block"]
            elif inputMode == "script":
                required = ["blocks"]
            
            for attribute in required:
                if attribute not in inputValue:
                    match attribute:
                        case "block":
                            inputValue["block"] = inputBlockDefault
                        case "text":
                            inputValue["text"] = inputTextDefault
                        case "blocks":
                            inputValue["blocks"] = inputBlocksDefault

            if inputValue.get("block") != None: # When the input has a block and it isn't None, check the block format
               validateBlock(path=path+[inputID]+["block"], data=inputValue["block"], context=context)
            
            if inputValue.get("blocks", []) != []:
                preparedData = {"position": [0,0], "blocks": inputValue["blocks"]}
                validateScript(path=path+[inputID], data=preparedData, context=context)
            
            # Specific value controls(None currently)
            match inputType: # type of the input
                case "broadcast"       : pass
                case "integer"         : pass
                case "positive integer": pass
                case "number"          : pass
                case "text"            : pass
                case "boolean"         : pass
                case "round"           : pass
                case "script"          : pass

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
            case "key"|"binary math operation"|"text operation"|"text case":
                match opcodeData["optionTypes"][optionID]:
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
                    case "unary math operation":
                        possibleValues = ["abs", "floor", "ceiling", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "ln", "log", "e ^", "10 ^"]
                    case "binary math operation":
                        possibleValues = ["^", "root", "log"]
                    case "text operation":
                        possibleValues = ["starts", "ends"]
                    case "text case":
                        possibleValues = ["upper", "lower"]
                if optionValue not in possibleValues:
                    raise formatError(path+[optionID], f"Must be one of {possibleValues}.")
            case "broadcast"|"string":
                if not isinstance(optionValue, str):
                    raise formatError(path+[optionID], f"Must be a string.")
            case "variable":
                if optionValue not in [var["name"] for var in context["scopeVariables"]]:
                    raise formatError(path+[optionID], f"Must be a defined variable.")
            case "list":
                if optionValue not in [list_["name"] for list_ in context["scopeLists"]]:
                    raise formatError(path+[optionID], f"Must be a defined list.")
            case "boolean":
                if not isinstance(optionValue, bool):
                    raise formatError(path+[optionID], f"Must be a boolean.")
            case "blockType":
                possibleValues = ["instruction", "lastInstruction", "stringReporter", "numberReporter", "booleanReporter"]
                if optionValue not in possibleValues:
                    raise formatError(path+[optionID], f"Must be one of {possibleValues}.")
