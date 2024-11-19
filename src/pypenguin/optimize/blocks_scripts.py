import json

from pypenguin.helper_functions import ikv, WhatIsGoingOnError, pp, customHash, escape_chars, generateCustomOpcode

from pypenguin.optimize.comments import translateComment

from pypenguin.database import opcodeDatabase

def translateVariableListBlock(data):
    # A variable or list block
    if data[0] == 12: # A magic value
        newData = {
            "opcode": "value of [VARIABLE]",
            "inputs": {},
            "options": {"VARIABLE": data[1]},
            "comment": None
        }
    elif data[0] == 13: # A magic value
        newData = {
            "opcode": "value of [LIST]",
            "inputs": {},
            "options": {"LIST": data[1]},
            "comment": None
        }
    else:
        raise WhatIsGoingOnError(data)
    return newData

def translateInputs(data, opcode, scriptData, blockChildrenPs, commentDatas, mutationDatas):
    newData = {}
    opcodeData = opcodeDatabase[opcode]
    for i,inputID,inputData in ikv(data):
        if "inputTranslation" in opcodeData:
            if inputID in opcodeData["inputTranslation"]:
                newInputID = opcodeData["inputTranslation"][inputID]
            else:
                newInputID = inputID
        else:
            newInputID = inputID
        if len(inputData) == 2:
            if   isinstance(inputData[1], str): # e.g. "CONDITION": [2, "b"]
                if opcode == "procedures_call":
                    inputType = "boolean"
                elif opcode == "control_create_clone_of":
                    inputType = "menu"
                else:
                    inputType = opcodeData["inputTypes"][newInputID]
                mode = "block-only" if inputType in ["boolean", "round", "menu"] else ("script" if inputType=="script" else None)
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
                "block": pointer,
            }
        elif mode == "block-and-text":
            newInputData = {
                "block": pointer,
                "text" : text, 
            }
        elif mode == "script":
            newInputData = {
                "blocks": translateScript(
                    data=scriptData,
                    ancestorP=inputData[1],
                    blockChildrenPs=blockChildrenPs,
                    commentDatas=commentDatas,
                    mutationDatas=mutationDatas,
                )
            }
        else: raise WhatIsGoingOnError(mode, inputType)

        newData[newInputID] = newInputData
    return newData

def translateOptions(data, opcode):
    newData = {}
    opcodeData = opcodeDatabase[opcode]
    for i,fieldID,fieldData in ikv(data):
        if "optionTranslation" in opcodeData:
            if fieldID in opcodeData["optionTranslation"]:
                optionID = opcodeData["optionTranslation"][fieldID]
            else:
                optionID = fieldID
        else:
            optionID = fieldID
        newFieldData = fieldData[0]
        newData[optionID] = newFieldData
    return newData

def translateScript(data, ancestorP, blockChildrenPs, commentDatas, mutationDatas):
    childrenDatas = {}
    for pointer in blockChildrenPs[ancestorP]:
        childrenDatas[pointer] = translateScript(
            data=data, 
            ancestorP=pointer, 
            blockChildrenPs=blockChildrenPs,
            commentDatas=commentDatas,
            mutationDatas=mutationDatas,
        )
    blockData = data[ancestorP] # Get the block's own data
    mutation = None
    if isinstance(blockData, dict):
        if blockData["opcode"] in ["procedures_definition", "procedures_definition_return", "procedures_prototype", "procedures_call"]:
            newOpcode = blockData["opcode"]
            if blockData["opcode"] == "procedures_call":
                inputs = translateInputs(
                    data=blockData["inputs"], 
                    opcode=blockData["opcode"], 
                    scriptData=data,
                    blockChildrenPs=blockChildrenPs,
                    commentDatas=commentDatas,
                    mutationDatas=mutationDatas,
                )
                for i,inputID,inputData in ikv(inputs):
                    if "block" in inputData:
                        if inputData["block"] != None:
                            if isinstance(inputData["block"], str):
                                subBlockData = childrenDatas[inputData["block"]][0]
                                pp(subBlockData)
                                inputs[inputID]["block"] = subBlockData
                            elif isinstance(inputData["block"], dict):
                                pass
            else:
                inputs = blockData["inputs"]
            options = blockData["fields"]
            if blockData["opcode"] in ["procedures_prototype", "procedures_call"]:
                mutation = blockData["mutation"]
        else:
            inputs = translateInputs(
                data=blockData["inputs"], 
                opcode=blockData["opcode"], 
                scriptData=data,
                blockChildrenPs=blockChildrenPs,
                commentDatas=commentDatas,
                mutationDatas=mutationDatas
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
        }
        if comment != None:
            newData["comment"] = comment
        if mutation != None:
            newData["mutation"] = mutation
    elif isinstance(blockData, list): # A variable or list block
        newData = translateVariableListBlock(blockData)

    newDatas = None
    if newData["opcode"] in ["procedures_definition", "procedures_definition_return"]:
        newDatas = translateScript(
            data=data,
            ancestorP=newData["inputs"]["custom_block"][1],
            blockChildrenPs=blockChildrenPs,
            commentDatas=commentDatas,
            mutationDatas=mutationDatas
        )
    elif newData["opcode"] == "procedures_prototype":
        mutationData = newData["mutation"]
        proccode = mutationData["proccode"]
        argumentNames = json.loads(mutationData["argumentnames"])
        customOpcode = generateCustomOpcode(proccode=proccode, argumentNames=argumentNames)

        match json.loads(mutationData["optype"]):
            case None       : blockType = "instruction"
            case "statement": blockType = "instruction"
            case "end"      : blockType = "lastInstruction"
            case "string"   : blockType = "stringReporter"
            case "number"   : blockType = "numberReporter"
            case "boolean"  : blockType = "booleanReporter"
            case _: raise Exception(mutationData["optype"], mutationData["returns"])
        oldData = newData
        newData = {
            "opcode": "define ...",
            "inputs": {},
            "options": {
                "customOpcode"   : customOpcode,
                "noScreenRefresh": json.loads(mutationData["warp"]),
                "blockType"      : blockType,
            },
        }
        if "comment" in oldData:
            newData["comment"] = oldData["comment"]
    elif newData["opcode"] == "procedures_call":
        proccode = newData["mutation"]["proccode"]
        mutationData = mutationDatas[proccode] # Get the full mutation data
        argumentNames = json.loads(mutationData["argumentnames"])
        argumentIDs = json.loads(mutationData["argumentids"])
        customOpcode = generateCustomOpcode(proccode=proccode, argumentNames=argumentNames)

        inputDatas = {}
        for i, inputID, inputData in ikv(newData["inputs"]):
            newInputID = argumentNames[argumentIDs.index(inputID)]
            inputDatas[newInputID] = inputData
        oldData = newData
        newData = {
            "opcode" : "call ...",
            "inputs" : inputDatas,
            "options": {
                "customOpcode": customOpcode,
            },
        }
        if "comment" in oldData:
            newData["comment"] = oldData["comment"]
    elif newData["opcode"] == "create clone of [TARGET]":
        target = newData["inputs"]["CLONE_OPTION"]["block"]["options"]["TARGET"]
        newData["options"]["TARGET"] = target
        del newData["inputs"]["CLONE_OPTION"]
    newDatas = [newData] if newDatas == None else newDatas
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

def getCustomBlockMutations(data):
    mutationDatas = {}
    for j, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    return mutationDatas
