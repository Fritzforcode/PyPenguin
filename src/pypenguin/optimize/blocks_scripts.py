from pypenguin.helper_functions import ikv, pp
from pypenguin.database import getOptimizedOpcode, getDeoptimizedOpcode, getOptimizedInputID, getInputMode, getInputModes, getOptimizedOptionID, getBlockType

import copy

def finishScripts(data):
    newScriptDatas = []
    for scriptData in data:
        newBlockDatas = []
        for blockData in scriptData["blocks"]:
            newBlockDatas.append(finishBlock(data=blockData))
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks"  : newBlockDatas,
        })
    return newScriptDatas

def finishBlock(data):
    blockType = getBlockType(
        opcode=getDeoptimizedOpcode(
            opcode=data["opcode"]
        ),
    )
    if blockType == "menu":
        return list(data["options"].values())[0]
        """ example:
        {
            "opcode": "#TOUCHING OBJECT MENU",
            "inputs": {},
            "options": {"TOUCHINGOBJECTMENU": "_mouse_"},
            "_info_": ...,
        }
        --> "_mouse_" """
    newInputDatas = {}
    for i, inputID, inputData in ikv(data["inputs"]):
        newInputData = copy.deepcopy(inputData)
        if inputData.get("block") != None:
            newInputData["block"]  = finishBlock(data=inputData["block"])
        if inputData.get("blocks") != None:
            newInputData["blocks"] = [finishBlock(data=subBlockData) for subBlockData in inputData["blocks"]]
        if inputData.get("option") != None:
            newInputData["option"] = finishBlock(data=inputData["option"])
        newInputDatas[inputID] = newInputData
    newData = data | {"inputs": newInputDatas}
    del newData["_info_"]
    return newData


def nestScripts(data):
    # Get all top level block ids
    topLevelIDs = []
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, list): continue
        if blockData["_info_"]["topLevel"]:
            topLevelIDs.append(blockID)
    
    # Account for that one bug(not my fault), where a block is falsely independent
    for i, blockID, blockData in ikv(data):
        #print(blockID, blockData)
        for j, inputID, inputData in ikv(blockData["inputs"]):
            #print(inputID, inputData)
            for reference in inputData["references"]:
                subBlockData = data[reference]
                if subBlockData["_info_"]["topLevel"]:
                    subBlockData["_info_"]["topLevel"] = False
                    del subBlockData["_info_"]["position"]
                    topLevelIDs.remove(reference)

    newScriptDatas = []
    for i, topLevelID in enumerate(topLevelIDs):
        scriptData = nestBlockRecursively(
            blockDatas=data,
            blockID=topLevelID,
        )
        newScriptData = {
            "position": scriptData[0]["_info_"]["position"],
            "blocks": scriptData,
        }
        newScriptDatas.append(newScriptData)
        #print("script end", 100*")")
        #pp(newScriptData)
    return newScriptDatas

def nestBlockRecursively(blockDatas, blockID):
    blockData = blockDatas[blockID]
    #pp(blockData)
    newInputDatas = {}
    for i, inputID, inputData in ikv(blockData["inputs"]):
        subBlockDatas = []
        #print(inputID, inputData)
        for j, reference in enumerate(inputData["references"]): 
            subBlockDatas.append(nestBlockRecursively(
                blockDatas=blockDatas,
                blockID=reference,
            ))

        if inputData["listBlock"] != None:
            subBlockDatas.append(inputData["listBlock"])
        
        #pp(subBlockDatas)
        blockCount = len(subBlockDatas)
        newInputData = {"mode": inputData["mode"]}
        match inputData["mode"]:
            case "block-and-text":
                assert blockCount in [0, 1]
                newInputData |= {
                    "block": subBlockDatas[0][0] if blockCount == 1 else None,
                    "text" : inputData["text"],
                }
            case "block-only":
                assert blockCount in [0, 1]
                newInputData |= {
                    "block": subBlockDatas[0][0] if blockCount == 1 else None,
                }
            case "script":
                assert blockCount in [0, 1]
                newInputData |= {
                    "blocks": subBlockDatas[0] if blockCount == 1 else [],
                }
            case "block-and-option":
                assert blockCount in [1, 2]
                newInputData |= {
                    "option": subBlockDatas[0][0] if blockCount == 1 else subBlockDatas[1][0],
                    "block" : None                if blockCount == 1 else subBlockDatas[0][0],
              }          
        newInputDatas[inputID] = newInputData
    
    
    
    newBlockData = blockData | {"inputs": newInputDatas}
    newBlockDatas = [newBlockData]
    if blockData["_info_"]["next"] != None:
        newBlockDatas += nestBlockRecursively(
            blockDatas=blockDatas,
            blockID=blockData["_info_"]["next"],
        )
    #print("ret", 50*"&")
    #pp(newBlockDatas)
    return newBlockDatas

def prepareBlocks(data):
    newData = {}
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, list): # For list blocks e.g. value of a variable
            newBlockData = prepareListBlock(data=blockData)
        else: # For normal blocks
            newBlockData = {
                "opcode"      : getOptimizedOpcode(opcode=blockData["opcode"]),
                "inputs"      : prepareInputs(
                    data=blockData["inputs"],
                    opcode=blockData["opcode"],
                ),
                "options"     : prepareOptions(
                    data=blockData["fields"],
                    opcode=blockData["opcode"],
                ),
                "_info_"      : {
                    "next"    : blockData["next"],
                    "topLevel": blockData["topLevel"],
                },
            }
            if "x" in blockData and "y" in blockData:
                newBlockData["_info_"]["position"] = [blockData["x"], blockData["y"]]
            #TODO: implement comments, custom blocks
            #if comment != None:
            #    newData["comment"] = comment
            #if mutation != None:
            #    newData["mutation"] = mutation
        newData[blockID] = newBlockData
    return newData

def prepareInputs(data, opcode):
    # Replace the old with the new input ids
    newData = {}
    for i, inputID, inputData in ikv(data):
        newInputID = getOptimizedInputID(
            opcode=opcode, 
            inputID=inputID,
        )
        newData[newInputID] = inputData
    data = newData
    
    # Optimize the input values
    newData = {}
    for i, inputID, inputData in ikv(data):
        #magicNumber = inputData[0]
        itemOneType = type(inputData[1])
        references = []
        listBlock  = None
        text       = None
        if   len(inputData) == 2:
            if   itemOneType == str: # e.g. "CONDITION": [2, "b"]
                # one block only, no text
                references.append(inputData[1])
            elif itemOneType == list: # e.g. "MESSAGE": [1, [10, "Bye!"]]
                # one block(currently empty) and text
                text = inputData[1][1]
        elif len(inputData) == 3:
            itemTwoType = type(inputData[2])
            if   itemOneType == str and itemTwoType == str: # e.g. "TOUCHINGOBJECTMENU": [3, "d", "e"]
                # two blocks(a menu, and a normal block) and no text
                references.append(inputData[1])
                references.append(inputData[2])
            elif itemOneType == str and itemTwoType == list: # e.g. 'OPERAND1': [3, 'e', [10, '']]
                # one block and text
                references.append(inputData[1])
                text = inputData[2][1]
            elif itemOneType == list: # e.g. 'VALUE': [3, [12, 'var', '=!vkqJLb6ODy(oqe-|ZN'], [10, '0']]
                # one list block and text
                listBlock = inputData[1]
                text = inputData[2][1]
        mode = getInputMode(
            opcode=opcode,
            inputID=inputID,
        )
        newInputData = {
            "mode"      : mode,
            "references": references,
            "listBlock" : listBlock,
            "text"      : text,
        }
        newData[inputID] = newInputData
    
    for i, inputID, inputMode in ikv(getInputModes(opcode)):
        if inputID not in newData:
            if inputMode in ["block-only", "script"]:
                newData[inputID] = {
                    "mode"      : inputMode,
                    "references": [],
                    "listBlock" : None,
                    "text"      : None,
                }
            else:
                raise Exception(inputMode)
    
    return newData    

def prepareOptions(data, opcode):
    newData = {}
    for i,optionID,optionData in ikv(data):
        newOptionID = getOptimizedOptionID(
            optionID=optionID,
            opcode=opcode,
        )
        newData[newOptionID] = optionData[0]
    return newData

def prepareListBlock(data):
    # A variable or list block
    if data[0] == 12: # A magic value
        newData = {
            "opcode": getOptimizedOpcode(opcode="special_variable_value"),
            "inputs": {},
            "options": {"VARIABLE": data[1]},
            "_info_"      : {
                "position": None,
                "next"    : None,
                "topLevel": False,
            },
        }
    elif data[0] == 13: # A magic value
        newData = {
            "opcode": getOptimizedOpcode(opcode="special_list_value"),
            "inputs": {},
            "options": {"LIST": data[1]},
            "_info_"      : {
                "position": None,
                "next"    : None,
                "topLevel": False,
            },
        }
    raise Exception() # Correct the following code
    if len(data) > 3:
        newData["_info_"]["position"] = data[4:6]
        newData["_info_"]["topLevel"] = True
        
        
    return newData

def getCustomBlockMutations(data):
    mutationDatas = {}
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    return mutationDatas
