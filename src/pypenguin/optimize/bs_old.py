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

def translateInputs(data, opcode, scriptData, blockChildrenIDs, commentDatas, mutationDatas):
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
                # Exceptions
                if opcode == "procedures_call":
                    inputType = "boolean"
                inputType = None
                if "menus" in opcodeData:
                    for menuData in opcodeData["menus"]:
                        if menuData["outer"] == inputID:
                            inputType = "menu"
                # Otherwise
                if inputType == None: 
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
            if   isinstance(inputData[1], str): 
                if isinstance(inputData[2], str): 
                    mode     = "block-and-option"
                    pointer  = inputData[1]
                    pointer2 = inputData[2]
                elif isinstance(inputData[2], list): # e.g. 'OPERAND1': [3, 'e', [10, '']]
                    mode    = "block-and-text"
                    pointer = inputData[1]
                    text    = inputData[2][1]
            elif isinstance(inputData[1], list): # e.g. 'VALUE': [3, [12, 'var', '=!vkqJLb6ODy(oqe-|ZN'], [10, '0']]
                mode    = "block-and-text"
                pointer = translateVariableListBlock(inputData[1])
                text    = inputData[2][1]
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
                    blockChildrenIDs=blockChildrenIDs,
                    commentDatas=commentDatas,
                    mutationDatas=mutationDatas,
                )
            }
        elif mode == "block-and-option":
            newInputData = {
                "block": pointer,
                "option": pointer2,
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
        newOptionData = fieldData[0]
        newData[optionID] = newOptionData
    return newData

def translateScript(data, ancestorP, blockChildrenIDs, commentDatas, mutationDatas):
    print(100*"=")
    pp(data)
    childrenDatas = {}
    for pointer in blockChildrenIDs[ancestorP]:
        childrenDatas[pointer] = translateScript(
            data=data, 
            ancestorP=pointer, 
            blockChildrenIDs=blockChildrenIDs,
            commentDatas=commentDatas,
            mutationDatas=mutationDatas,
        )
    blockData = data[ancestorP] # Get the block's own data
    mutation = None
    pp(childrenDatas)
    if isinstance(blockData, dict):
        if blockData["opcode"] in ["procedures_definition", "procedures_definition_return", "procedures_prototype", "procedures_call"]:
            newOpcode = blockData["opcode"]
            if blockData["opcode"] == "procedures_call":
                inputs = translateInputs(
                    data=blockData["inputs"], 
                    opcode=blockData["opcode"], 
                    scriptData=data,
                    blockChildrenIDs=blockChildrenIDs,
                    commentDatas=commentDatas,
                    mutationDatas=mutationDatas,
                )
                for i,inputID,inputData in ikv(inputs):
                    if inputData.get("block") != None:
                        if isinstance(inputData["block"], str):
                            subBlockData = childrenDatas[inputData["block"]][0]
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
                blockChildrenIDs=blockChildrenIDs,
                commentDatas=commentDatas,
                mutationDatas=mutationDatas
            )
            for i,inputID,inputData in ikv(inputs):
                if inputData.get("block") != None:
                    if isinstance(inputData["block"], str):
                        subBlockData = childrenDatas[inputData["block"]][0]
                        inputs[inputID]["block"] = subBlockData
                    elif isinstance(inputData["block"], dict):
                        pass
                if inputData.get("option") != None:
                    print("bef")
                    pp(inputData)
                    if isinstance(inputData["option"], str):
                        subBlockID = inputData["option"]
                        childrenDatas[subBlockID] = translateScript(
                            data=data,
                            ancestorP=subBlockID,
                            blockChildrenIDs=blockChildrenIDs,
                            commentDatas=commentDatas,
                            mutationDatas=mutationDatas,
                        )
                        subBlockData = childrenDatas[subBlockID]
                        pp(subBlockData)
                        #inputs[inputID]["option"] = subBlockData
                    elif isinstance(inputData["option"], dict):
                        pass
                    print("aft")
                    pp(inputData)
                    raise WhatIsGoingOnError()

                
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
            blockChildrenIDs=blockChildrenIDs,
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
    
    if isinstance(blockData, dict):
        opcodeData = opcodeDatabase[blockData["opcode"]]
        if "menus" in opcodeData:
            for menuData in opcodeData["menus"]:
                newID     = menuData["new"]
                outerID   = menuData["outer"]
                innerID   = menuData["inner"]
                menuValue = newData["inputs"][outerID]["block"]["options"][innerID]
                del newData["inputs"][outerID]
                newData["inputs"][newID] = {"option": menuValue}
    
    newDatas = [newData] if newDatas == None else newDatas
    if isinstance(blockData, dict):
        if blockData["next"] != None: #if the block does have a neighbour
            newDatas += childrenDatas[blockData["next"]]
    
    if isinstance(blockData, list):
        returnValue = {"position": [blockData[3], blockData[4]], "blocks": newDatas} 
    elif blockData["topLevel"] == True:
        returnValue = {"position": [blockData["x"], blockData["y"]], "blocks": newDatas} 
    else:
        returnValue = newDatas
    return returnValue
    
def generateBlockChildrenIDs(data):
    blockParentIDs = {}
    for i,blockID,blockData in ikv(data):
        if blockID not in blockParentIDs:
            if isinstance(blockData, dict):
                blockParentIDs[blockID] = blockData["parent"]
            elif isinstance(blockData, list):
                blockParentIDs[blockID] = None
        
        # For a special case when "parent" is wrongfully None e.g. [3, "d", "e"]
        for i, inputID, inputData in ikv(blockData["inputs"]):
            if len(inputData) != 3: continue
            if inputData[0]   != 3: continue
            if not isinstance(inputData[1], str): continue
            if not isinstance(inputData[2], str): continue
            blockParentIDs[inputData[2]] = blockID 
    blockChildrenIDs = {k:[] for k in data.keys()} # Create an empty dict which records each block's children
    # Add each block to their parent's children list
    ancestorIDs = []
    for i,childP,parentP in ikv(blockParentIDs):
        if parentP != None:
            blockChildrenIDs[parentP].append(childP)
        if parentP == None:
            ancestorIDs.append(childP)
    return ancestorIDs, blockChildrenIDs

def getCustomBlockMutations(data):
    mutationDatas = {}
    for j, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    return mutationDatas
