from helper_functions import ikv, WhatIsGoingOnError, readJSONFile

from optimize.comments import translateComment

from database import opcodeDatabase


def translateInputs(data):
    newData = {}
    for i,inputID,inputData in ikv(data):
        if len(inputData) == 2:
            if   isinstance(inputData[1], str): # eg. "CONDITION": [2, "b"]
                mode = "block-only"
                pointer = inputData[1]
                text = None
            elif isinstance(inputData[1], list): # eg. "MESSAGE": [1, [10, "Bye!"]]
                mode = "block-and-text"
                pointer = None
                text = inputData[1][1]
            else:
                raise WhatIsGoingOnError(inputData)
        elif len(inputData) == 3:
            if   isinstance(inputData[1], str): # ex 'OPERAND1': [3, 'e', [10, '']]
                mode = "block-and-text"
                pointer = inputData[1]
                text = inputData[2][1]
            else:
                raise WhatIsGoingOnError(inputData)
        else:
            raise WhatIsGoingOnError(inputData)
        if mode == "block-only":
            newInputData = {
                "mode": mode,
                "block": pointer,
            }
        elif mode == "block-and-text":
            newInputData = {
                "mode" : mode,
                "block": pointer,
                "text" : text, 
            }
        else: raise WhatIsGoingOnError()
        newData[inputID] = newInputData
    return newData

def translateOptions(opcode, data):
    newData = {}
    for i,fieldID,fieldData in ikv(data):
        opcodeData = opcodeDatabase[opcode]
        match opcodeData["optionTypes"][fieldID]:
            case "variable":
                newFieldData = fieldData[0]
            case "list":
                newFieldData = fieldData[0]
            case "broadcast":
                newFieldData = fieldData[0]
            case "key":
                newFieldData = fieldData[0]
            case _: raise WhatIsGoingOnError(opcodeData["optionTypes"][fieldID])
        newData[fieldID] = newFieldData
    return newData

def translateScript(data, ancestorP, blockChildrenPs, commentDatas):
    childrenDatas = {}
    for pointer in blockChildrenPs[ancestorP]:
        childrenDatas[pointer] = translateScript(
            data=data, 
            ancestorP=pointer, 
            blockChildrenPs=blockChildrenPs,
            commentDatas=commentDatas
        )
    blockData = data[ancestorP] # Get the block's own data
    inputs = translateInputs(blockData["inputs"])
    for i,inputID,inputData in ikv(inputs):
        if "block" in inputData:
            if inputData["block"] != None:
                inputs[inputID]["block"] = childrenDatas[inputData["block"]][0]
    options = translateOptions(opcode=blockData["opcode"], data=blockData["fields"])
    newOpcode = opcodeDatabase[blockData["opcode"]]["newOpcode"]
    comment = None
    for commentData in commentDatas.values():
        if commentData["blockId"] == ancestorP:
            comment = translateComment(data=commentData)
    newData = {
        "opcode"      : newOpcode,
        "inputs"      : inputs,
        "options"     : options,
        "comment"     : comment,
    }

    newDatas = [newData]
    if blockData["next"] != None: #if the block does not have a neighbour
        newDatas += childrenDatas[blockData["next"]]
    
    if blockData["topLevel"] == True:
        return {"position": [blockData["x"], blockData["y"]], "blocks": newDatas} 
    else:
        return newDatas

def generateBlockChildrenPs(data):
    blockParentPs = {k:v["parent"] for i,k,v in ikv(data)} # Get all block's parents
    blockChildrenPs = {k:[] for k in data.keys()} # Create an empty dict which records each block's children
    # Add each block to their parent's children list
    ancestorPs = []
    for i,childP,parentP in ikv(blockParentPs):
        if parentP != None:
            blockChildrenPs[parentP].append(childP)
        opcodeData = opcodeDatabase[data[childP]["opcode"]]
        if parentP == None:
            ancestorPs.append(childP)
    return ancestorPs, blockChildrenPs
