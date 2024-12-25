from pypenguin.helper_functions import ikv, parseCustomOpcode, pp
from pypenguin.validate.constants import validateSchema, formatError, inputSchema, blockSchema, scriptSchema
from pypenguin.validate.comments import validateComment
from pypenguin.database import *

def validateScript(path, data, context, isNested=True):
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
        print(block, blockType)
        if isNested:
            if blockType in ["stringReporter", "numberReporter", "booleanReporter"]:
                raise formatError(path+[i], "Reporter blocks are not allowed in the 'blocks' attribute of an input.")
            if blockType == "hat":
                raise formatError(path+[i], "Hat blocks are not allowed in the 'blocks' attribute of an input.")
        
        if   (blockType in ["stringReporter", "numberReporter", "booleanReporter"]) and (len(data["blocks"]) > 1):
            raise formatError(path+[i], "A reporter block must be the only block in it's script.")
        elif blockType == "hat" and i > 0:
            raise formatError(path+[i], "A hat block must to be the first block in it's script.")
        elif blockType == "lastInstruction" and i+1 in range(len(data["blocks"])): # when there is a next block
            raise formatError(path+[i], "An ending block must be the last block in it's script.")

def validateBlock(path, data, context, expectedShape=None):
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
                    validateBlock(
                        path=path+[inputID]+["block"], 
                        data=inputValue["block"], 
                        context=context,
                        expectedShape="booleanReporter" if inputType == "boolean" else "stringReporter",
                    )
                
                if inputValue.get("blocks", []) != []:
                    preparedData = {"position": [0,0], "blocks": inputValue["blocks"]}
                    validateScript(path=path+[inputID], data=preparedData, context=context, isNested=True)
                
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
    def makeString(possibleValues):
        if possibleValues == []:
            string = "No possible values."
        else:
            string = ""
            for value in possibleValues:
                string += "\n- "
                string += repr(value)
        return string
    def validateCategory(path, data, suggestion):
        if data != suggestion:
            raise formatError(path, f"Must be '{suggestion}'.")
    match optionType:
        case "broadcast"|"reporter name"|"opcode":
            validateCategory(path+[0], data[0], "value")
            if not isinstance(data[1], str):
                raise formatError(path, f"Must be a string.")
        case "variable":
            possibleValues = context["scopeVariables"]
            possibleValuesString = makeString(possibleValues)
            if data not in possibleValues:
                raise formatError(path, f"Must be a defined variable. Must be one of these: {possibleValuesString}")
        case "list":
            possibleValues = context["scopeLists"]
            possibleValuesString = makeString(possibleValues)
            if data not in possibleValues:
                raise formatError(path, f"Must be a defined list. Must be one of these: {possibleValuesString}")
        case "boolean":
            validateCategory(path+[0], data[0], "value")
            if not isinstance(data[1], bool):
                raise formatError(path, f"Must be a boolean.")
        case _:
            possibleValues = getOptimizedOptionValuesUsingContext(
                optionType=optionType,
                context=context,
                inputDatas=inputDatas,
            )
            #pp(possibleValues)
            possibleValuesString = makeString(possibleValues)
            if data not in possibleValues:
                raise formatError(path, f"Must be one of these: {possibleValuesString}")

