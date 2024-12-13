from pypenguin.helper_functions import ikv, parseCustomOpcode, pp
from pypenguin.validate.constants import validateSchema, formatError, inputSchema, blockSchema, scriptSchema
from pypenguin.validate.comments import validateComment
from pypenguin.database import *

def validateScript(path, data, context):
    # Check script format
    validateSchema(pathToData=path, data=data, schema=scriptSchema)

    # Check block formats
    for i, block in enumerate(data["blocks"]):
        validateBlock(
            path=path+["blocks"]+[i], 
            data=block, 
            context=context,
        )
        
        oldOpcode = getDeoptimizedOpcode(opcode=block["opcode"])
        blockType = getBlockType(opcode=oldOpcode)
        if (blockType in ["textReporter", "numberReporter", "booleanReporter"]) and (len(data["blocks"]) > 1):
            raise formatError(path, "A script whose first block is a reporter mustn't have more than one block.")

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
    validateInputs(
        path=path+["inputs"], 
        data=data["inputs"],
        opcode=opcode, 
        context=context, 
    )
    validateOptions(
        path=path+["options"],
        data=data["options"],
        opcode=opcode,
        context=context,
        inputDatas=data["inputs"],
    )
    if opcode == "call custom block":
        validateCallInputs(
            path=path+["inputs"], 
            data=data["inputs"],
            optionDatas=data["options"],
        )

def validateInputs(path, data, opcode, context):
    oldOpcode       = getDeoptimizedOpcode(opcode=opcode)
    allowedInputIDs = list(getInputTypes(opcode=oldOpcode).keys()) # List of inputs which are defined for the specific opcode
    if opcode != "call custom block": # Inputs in the call custom block block are custom
        for i, inputID, inputValue in ikv(data):
            if inputID not in allowedInputIDs:
                raise formatError(path, f"Input '{inputID}' is not defined for a block with opcode '{opcode}'.")
        for inputID in allowedInputIDs:
            inputMode = getInputMode(
                opcode=oldOpcode,
                inputID=inputID,
            )
            if inputMode not in ["block-only", "script"]:
                if inputID not in data:
                    raise formatError(path, f"A block with opcode '{opcode}' must have the input '{inputID}'.")

        inputTypes = getInputTypes(opcode=oldOpcode)
    
        # Check input formats
        for inputID in data:
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
                elif inputMode in ["block-and-option", "block-and-hybrid-option"]:
                    required = ["option"]
                
                for attribute in required:
                    if attribute not in inputValue:
                        match attribute:
                            case "block":
                                inputValue["block"] = inputBlockDefault
                            case "text":
                                inputValue["text"] = inputTextDefault
                            case "blocks":
                                inputValue["blocks"] = inputBlocksDefault
                            case "option":
                                raise formatError(path=path+[inputID], message="Must have the attribute 'option'.")

                if inputValue.get("block") != None: # When the input has a block and it isn't None, check the block format
                    validateBlock(path=path+[inputID]+["block"], data=inputValue["block"], context=context)
                
                if inputValue.get("blocks", []) != []:
                    preparedData = {"position": [0,0], "blocks": inputValue["blocks"]}
                    validateScript(path=path+[inputID], data=preparedData, context=context)
                
                if inputValue.get("option") != None:
                    validateOptionValue(
                        path=path+[inputID]+["option"],
                        data=inputValue["option"],
                        opcode=opcode,
                        optionType=inputType, # Might need to be changed
                        context=context,
                        inputDatas=data,
                    )

def validateCallInputs(path, data, optionDatas):
    proccode, inputTypes = parseCustomOpcode(optionDatas["customOpcode"][1])
    inputTypes = {k: ("text" if v==str else "boolean") for i,k,v in ikv(inputTypes)}
    for i, inputID, inputType in ikv(inputTypes):
        if inputType == "text" and inputID not in data:
            raise formatError(path, f"A custom block with custom opcode '{optionDatas['customOpcode']}' must have the input '{inputID}'.")
    
    # Check input formats
    for inputID in data:
        if inputID not in inputTypes:
            raise formatError(path, f"Input '{inputID}' is not defined for a custom block with custom opcode '{optionDatas['customOpcode']}'.")

def validateOptions(path, data, opcode, context, inputDatas):
    oldOpcode        = getDeoptimizedOpcode(opcode=opcode)
    allowedOptionIDs = list(getOptionTypes(opcode=oldOpcode).keys()) # List of inputs which are defined for the specific opcode
    for i, optionID, optionValue in ikv(data):
        if optionID not in allowedOptionIDs:
            raise formatError(path, f"Option '{optionID}' is not defined for a block with opcode '{opcode}'.")
    for optionID in allowedOptionIDs:
        if optionID not in data:
            raise formatError(path, f"A block with opcode '{opcode}' must have the option '{optionID}'.")

        
        optionType = getOptionType(
            opcode=oldOpcode,
            optionID=optionID,
        )
        optionValue = data[optionID]
        validateOptionValue(
            path=path+[optionID],
            data=optionValue,
            opcode=opcode,
            optionType=optionType,
            context=context,
            inputDatas=inputDatas,
        )

def validateOptionValue(path, data, opcode, optionType, context, inputDatas):
    match optionType:
        case "broadcast"|"string"|"opcode":
            if not isinstance(data, str):
                raise formatError(path, f"Must be a string.")
        case "variable":
            possibleValues = context["scopeVariables"]
            if data not in possibleValues:
                raise formatError(path, f"Must be a defined variable. Must be one of these: {possibleValues}")
        case "list":
            possibleValues = context["scopeLists"]
            if data not in possibleValues:
                raise formatError(path, f"Must be a defined list. Must be one of these: {possibleValues}")
        case "boolean":
            if not isinstance(data, bool):
                raise formatError(path, f"Must be a boolean.")
        case _:
            match optionType:
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
                case "power|root|log":
                    possibleValues = ["^", "root", "log"]
                case "root|log":
                    possibleValues = ["root", "log"]
                case "text method":
                    possibleValues = ["starts", "ends"]
                case "text case":
                    possibleValues = ["upper", "lower"]
                case "stop script target":
                    possibleValues = ["all", "this script", "other scripts in sprite"]
                case "stage || other sprite":
                    possibleValues = ["_stage_"] + context["otherSprites"]
                case "cloning target":
                    possibleValues = context["cloningTargets"]
                case "up|down":
                    possibleValues = ["up", "down"]
                case "loudness or timer":
                    possibleValues = ["LOUDNESS", "TIMER"]
                case "mouse || other sprite":
                    possibleValues = ["_mouse_"] + context["otherSprites"]
                case "mouse|edge || other sprite":
                    possibleValues = ["_mouse_", "_edge_"] + context["otherSprites"]
                case "mouse|edge|myself || other sprite":
                    possibleValues = ["_mouse_", "_edge_", "_myself_"] + context["otherSprites"]
                case "coordinate":
                    possibleValues = ["x", "y"]
                case "drag mode":
                    possibleValues = ["draggable", "not draggable"]
                case "mutable sprite property":
                    match opcode:
                        case "set [PROPERTY] of ([TARGET]) to (VALUE)":
                            if inputDatas["TARGET"]["option"] == "_stage_":
                                nameKey = None
                            else:
                                nameKey = inputDatas["TARGET"]["option"]
                    if nameKey == None:
                        possibleValues = ["backdrop", "volume"] + context["globalVariables"]
                    else:
                        possibleValues = ["x position", "y position", "direction", "costume", "size", "volume"] + context["localVariables"][nameKey]
                case "readable sprite property":
                    match opcode:
                        case "[PROPERTY] of ([TARGET])":
                            if inputDatas["TARGET"]["option"] == "_stage_":
                                nameKey = None
                            else:
                                nameKey = inputDatas["TARGET"]["option"]
                    if nameKey == None:
                        possibleValues = ["backdrop #", "backdrop name", "volume"] + context["globalVariables"]
                    else:
                        possibleValues = ["x position", "y position", "direction", "costume #", "costume name", "layer", "size", "volume"] + context["localVariables"][nameKey]
                case "time property":
                    possibleValues = ["YEAR", "MONTH", "DATE", "DAYOFWEEK", "HOUR", "MINUTE", "SECOND", "TIMESTAMP"]
                case "finger index":
                    possibleValues = ["1", "2", "3", "4", "5"]
                case "random|mouse || other sprite":
                    possibleValues = ["_random_", "_mouse_"] + context["otherSprites"]
                case "rotation style":
                    possibleValues = ["left-right", "up-down", "don't rotate", "look at", "all around"]
                case "stage zone":
                    possibleValues = ["bottom-left", "bottom", "bottom-right", "top-left", "top", "top-right", "left", "right"]
                case "text bubble color property":
                    possibleValues = ["BUBBLE_STROKE", "BUBBLE_FILL", "TEXT_FILL"]
                case "text bubble property":
                    possibleValues = ["MIN_WIDTH", "MAX_LINE_WIDTH", "STROKE_WIDTH", "PADDING", "CORNER_RADIUS", "TAIL_HEIGHT", "FONT_HEIGHT_RATIO", "texlim"]
                case "sprite effect":
                    possibleValues = ["COLOR", "FISHEYE", "WHIRL", "PIXELATE", "MOSAIC", "BRIGHTNESS", "GHOST", "SATURATION", "RED", "GREEN", "BLUE", "OPAQUE"]
                case "costume":
                    possibleValues = context["costumes"]
                case "backdrop":
                    possibleValues = context["backdrops"]
                case "costume property":
                    possibleValues = ["width", "height", "rotation center x", "rotation center y", "drawing mode"]
                case ""myself || other sprite"":
                    possibleValues = ["_myself_"] + context["otherSprites"]
                case "front or back":
                    possibleValues = ["front", "back"]
                case "forward or backward":
                    possibleValues = ["forward", "backward"]
                case "infront or behind":
                    possibleValues = ["infront", "behind"]
                case "number or name":
                    possibleValues = ["number", "name"]
                case "sound":
                    possibleValues = context["sounds"]
                case "sound effect":
                    possibleValues = ["PITCH", "PAN"]
                case "blockType":
                    possibleValues = ["instruction", "lastInstruction", "textReporter", "numberReporter", "booleanReporter"]
            if data not in possibleValues:
                raise formatError(path, f"Must be one of {possibleValues}.")
