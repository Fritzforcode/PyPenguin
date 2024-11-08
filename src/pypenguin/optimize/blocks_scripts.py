from helper_functions import ikv, WhatIsGoingOnError, pp

from optimize.comments import translateComment

from database import opcodeDatabase

def translateVariableListBlock(data):
    # A variable or list block
    if data[0] == 12: # A magic value
        newData = {
            "opcode": "VARIABLE",
            "inputs": {},
            "options": {"VARIABLE": data[1]},
            "comment": None
        }
    elif data[0] == 13: # A magic value
        newData = {
            "opcode": "LIST",
            "inputs": {},
            "options": {"LIST": data[1]},
            "comment": None
        }
    else:
        raise WhatIsGoingOnError(data)
    return newData

def translateInputs(data, opcode, scriptData, blockChildrenPs, commentDatas):
    newData = {}
    for i,inputID,inputData in ikv(data):   
        if len(inputData) == 2:
            if   isinstance(inputData[1], str): # e.g. "CONDITION": [2, "b"]
                inputType = opcodeDatabase[opcode]["inputTypes"][inputID]
                mode = "block-only" if inputType=="boolean" else ("script" if inputType=="script" else None)
                pointer = inputData[1]
                text = None
            elif isinstance(inputData[1], list): # e.g. "MESSAGE": [1, [10, "Bye!"]]
                mode = "block-and-text"
                pointer = None
                text = inputData[1][1]
            else:
                raise WhatIsGoingOnError(inputData)
        elif len(inputData) == 3:
            if   isinstance(inputData[1], str): # e.g. 'OPERAND1': [3, 'e', [10, '']]
                mode = "block-and-text"
                pointer = inputData[1]
                text = inputData[2][1]
            elif isinstance(inputData[1], list): # e.g. 'VALUE': [3, [12, 'var', '=!vkqJLb6ODy(oqe-|ZN'], [10, '0']]
                mode = "block-and-text"
                pointer = translateVariableListBlock(inputData[1])
                text = inputData[2][1]
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
        elif mode == "script":
            newInputData = {
                "mode": mode,
                "blocks": translateScript(
                    data=scriptData,
                    ancestorP=inputData[1],
                    blockChildrenPs=blockChildrenPs,
                    commentDatas=commentDatas,
                )
            }
        else: raise WhatIsGoingOnError(mode, inputType)

        newData[inputID] = newInputData
    return newData

def translateOptions(data, opcode):
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
    if isinstance(blockData, dict): # A normal block
        inputs = translateInputs(
            data=blockData["inputs"], 
            opcode=blockData["opcode"], 
            scriptData=data,
            blockChildrenPs=blockChildrenPs,
            commentDatas=commentDatas,
        )
        for i,inputID,inputData in ikv(inputs):
            if "block" in inputData:
                if inputData["block"] != None:
                    if isinstance(inputData["block"], str):
                        inputs[inputID]["block"] = childrenDatas[inputData["block"]][0]
                    elif isinstance(inputData["block"], dict):
                        pass
        options = translateOptions(data=blockData["fields"], opcode=blockData["opcode"])
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
    elif isinstance(blockData, list): # A variable or list block
        newData = translateVariableListBlock(blockData)

    newDatas = [newData]
    if isinstance(blockData, dict):
        if blockData["next"] != None: #if the block does have a neighbour
            newDatas += childrenDatas[blockData["next"]]
    
    if isinstance(blockData, list):
        return {"position": [blockData[3], blockData[4]], "blocks": newDatas} 
    elif blockData["topLevel"] == True:
        return {"position": [blockData["x"], blockData["y"]], "blocks": newDatas} 
    else:
        return newDatas

def generateBlockChildrenPs(data):
    blockParentPs = {}
    for i,k,v in ikv(data):
        if isinstance(v, dict):
            blockParentPs[k] = v["parent"]
        elif isinstance(v, list):
            blockParentPs[k] = None
    blockChildrenPs = {k:[] for k in data.keys()} # Create an empty dict which records each block's children
    # Add each block to their parent's children list
    ancestorPs = []
    for i,childP,parentP in ikv(blockParentPs):
        if parentP != None:
            blockChildrenPs[parentP].append(childP)
        if parentP == None:
            ancestorPs.append(childP)
    return ancestorPs, blockChildrenPs
