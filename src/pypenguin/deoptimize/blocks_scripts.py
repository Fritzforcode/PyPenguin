import json, copy

from pypenguin.helper_functions import ikv, pp, WhatIsGoingOnError, numberToLiteral, newTempSelector, generateRandomToken, parseCustomOpcode, stringToToken
from pypenguin.deoptimize.options import translateOptions
from pypenguin.deoptimize.comments import translateComment
from pypenguin.database import *


def unfinishScripts(data):
    newScriptDatas = []
    for scriptData in data:
        newBlockDatas = []
        for i, blockData in enumerate(scriptData["blocks"]):
            newBlockDatas.append(unfinishBlock(
                data=blockData,
                parentOpcode=None,
                position=scriptData["position"] if i == 0 else None
            ))
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks"  : newBlockDatas,
        })
    return newScriptDatas

def generateMenu(data, parentOpcode, inputID):
    opcode = getDeoptimizedOpcode(opcode=parentOpcode)
    menu = getMenu(
        opcode=opcode,
        inputID=inputID,
    )
    menuOpcode = getOptimizedOpcode(opcode=menu["menuOpcode"])
    newData = {
        "opcode" : menuOpcode,
        "inputs" : {},
        "options": {
            menu["inner"]: data,
        },
    }
    return newData
    """ "_mouse_" ->
    {
        "opcode": "#TOUCHING OBJECT MENU",
        "inputs": {},
        "options": {"TOUCHINGOBJECTMENU": "_mouse_"},
        "_info_": ...,
    }"""

def unfinishBlock(data, parentOpcode, position=None, isOption=False, inputID=None):
    #print("start ufblock", 100*"{")
    #pp(data)
    if isinstance(data, str):
        if not isOption: raise Exception()
        # When the block is a menu value
        data = generateMenu(
            data=data,
            parentOpcode=parentOpcode,
            inputID=inputID,
        )
    newInputDatas = {}
    for i, inputID, inputData in ikv(data["inputs"]):
        if inputData["mode"] == "block-and-hybrid-option":
            inputData["text"] = inputData["option"]
            del inputData["option"]
        newInputData = copy.deepcopy(inputData)
        if inputData.get("block") != None:
            newInputData["block"]  = unfinishBlock(
                data=inputData["block"],
                parentOpcode=data["opcode"],
            )
        if inputData.get("blocks") != None:
            newInputData["blocks"] = [unfinishBlock(
                data=subBlockData,
                parentOpcode=data["opcode"],
            ) for subBlockData in inputData["blocks"]]
        if inputData.get("option") != None:
            newInputData["option"] = unfinishBlock(
                data=inputData["option"],
                parentOpcode=data["opcode"],
                isOption=True,
                inputID=inputID,
            )
        newInputDatas[inputID] = newInputData
    newData = data | {
        "inputs": newInputDatas,
        "_info_": {
            "position": position,
            "topLevel": position != None,
        },
    }
    #print("stop fblock", 100*"}")
    #pp(newData)
    return newData

def flattenScripts(data):
    newBlockDatas = {}
    for scriptData in data:
        # Generate IDs for the blocks
        newBlockDatas |= flattenBlocks(
            data=scriptData["blocks"],
        )
    return newBlockDatas

def flattenBlocks(data, parentID=None, firstID=None):
    range_ = range(len(data))
    blockIDs = [newTempSelector() for i in range_]
    if firstID != None:
        blockIDs[0] = firstID
    newBlockDatas = {}
    for i, blockData in enumerate(data):
        blockID = blockIDs[i]
        if i - 1 in range_: # When the block has a upwards neighbour
            parentID = blockIDs[i - 1]
        elif i == 0:
            parentID = parentID
        if i + 1 in range_: # When the block has a downwards neighbour
            nextID = blockIDs[i + 1]
        else:
            nextID = None
        
        newBlockDatas |= flattenBlock(
            data=blockData,
            blockID=blockID,
            parentID=parentID,
            nextID=nextID,
        )
    return newBlockDatas

def flattenBlock(data, blockID, parentID, nextID):
    #print(100*"{")
    #pp(data)
    # Transform inputs
    newBlockDatas = {}
    newInputDatas = {}
    for j, inputID, inputData in ikv(data["inputs"]):
        references = []
        listBlock = None
        if inputData.get("block") != None:
            if inputData["block"]["opcode"] in [
                getOptimizedOpcode(opcode="special_variable_value"),
                getOptimizedOpcode(opcode="special_list_value"),
            ]:
                # If a list block, dont make it independent; instead use "listBlock"
                listBlock = inputData["block"]
                # Optional just in case
                listBlock["_info_"] |= {
                    "parent": blockID,
                    "next"  : None
                }
            else:
                subBlockID = newTempSelector()
                references.append(subBlockID)
                newBlockDatas |= flattenBlock(
                    data=inputData["block"],
                    blockID=subBlockID,
                    parentID=blockID,
                    nextID=None,
                )
        if inputData.get("blocks", []) != []:
            subBlockID = newTempSelector()
            references.append(subBlockID)
            newBlockDatas |= flattenBlocks(
                data=inputData["blocks"],
                parentID=blockID,
                firstID=subBlockID,
            )
        if inputData.get("option") != None:
            subBlockID = newTempSelector()
            references.append(subBlockID)
            newBlockDatas |= flattenBlock(
                data=inputData["option"],
                blockID=subBlockID,
                parentID=blockID,
                nextID=None,
            )
        newInputData = {
            "mode"      : inputData["mode"],
            "references": references,
            "listBlock" : listBlock,
            "text"      : inputData.get("text"),
        }
        newInputDatas[inputID] = newInputData

    newBlockData = {
        "opcode" : data["opcode"],
        "inputs" : newInputDatas,
        "options": data["options"],
        "_info_" : data["_info_"] | {
            "parent"  : parentID,
            "next"    : nextID,
        }
    }
    newBlockDatas[blockID] = newBlockData
    #print(100*"}")
    #pp(newBlockDatas)
    return newBlockDatas

def restoreBlocks(data, spriteName):
    #pp(data)
    newBlockDatas = {}
    for i, blockID, blockData in ikv(data):
        opcode = getDeoptimizedOpcode(opcode=blockData["opcode"])
        
        if opcode in ["special_variable_value", "special_list_value"]:
            newBlockData = restoreListBlock(
                data=blockData,
                spriteName=spriteName,
            )
        else:
            blockType = getBlockType(opcode=opcode)
            if blockType == "menu":
                hasShadow = True
            else:
                hasShadow = False
            
            newBlockData = {
                "opcode"  : opcode,
                "next"    : blockData["_info_"]["next"],
                "parent"  : blockData["_info_"]["parent"],
                "inputs"  : restoreInputs(
                    data=blockData["inputs"],
                    opcode=opcode,
                    spriteName=spriteName,
                ),
                "fields"  : translateOptions(
                    data=blockData["options"],
                    opcode=opcode,
                    spriteName=spriteName,
                ),
                "shadow"  : hasShadow,
                "topLevel": blockData["_info_"]["topLevel"],
            }
            if blockData["_info_"]["position"] != None:
                position = blockData["_info_"]["position"]
                newBlockData |= {"x": position[0], "y": position[1]}
        newBlockDatas[blockID] = newBlockData
    return newBlockDatas

def restoreInputs(data, opcode, spriteName):
    newInputDatas = {}
    for i, inputID, inputData in ikv(data):
        inputType = getInputType(
            opcode=opcode,
            inputID=inputID
        )
        inputMode = getInputMode(
            opcode=opcode,
            inputID=inputID
        )
        #print(inputID, inputType, inputMode, inputData)
        
        subBlocks     = inputData["references"]
        if inputData["listBlock"] != None:
            subBlocks.insert(0, restoreListBlock(
                data=inputData["listBlock"],
                spriteName=spriteName,
            ))
        subBlockCount = len(subBlocks)
        match inputMode:
            case "block-and-text"|"block-and-hybrid-option":
                magicNumber = getInputMagicNumber(inputType=inputType)
                textData = [magicNumber, inputData["text"]]
                if inputMode == "block-and-hybrid-option":
                    token = stringToToken(inputData["text"])
                    textData.append(token)
                if   subBlockCount == 0:
                    newInputData = [1, textData]
                elif subBlockCount == 1:
                    newInputData = [3, subBlocks[0], textData]
            case "block-only"|"script":
                if   subBlockCount == 0:
                    newInputData = None
                elif subBlockCount == 1:
                    newInputData = [2, subBlocks[0]]
            case "block-and-option":
                if   subBlockCount == 1:
                    newInputData = [1, subBlocks[0]]
                elif subBlockCount == 2:
                    newInputData = [3, subBlocks[0],  subBlocks[1]]
        
        
        newInputID = getDeoptimizedInputID(
            opcode=opcode,
            inputID=inputID,
        )
        if newInputData != None:
            newInputDatas[newInputID] = newInputData
    return newInputDatas

def restoreListBlock(data, spriteName):
    if   data["opcode"] == getOptimizedOpcode(opcode="special_variable_value"):
        magicNumber = 12
        value = data["options"]["VARIABLE"]
    elif data["opcode"] == getOptimizedOpcode(opcode="special_list_value"    ):
        magicNumber = 13
        value = data["options"]["LIST"]
    
    token = stringToToken(value, spriteName=spriteName)
    newData = [magicNumber, value, token]
    if data["_info_"]["topLevel"]:
        newData += data["_info_"]["position"]
    return newData

def finishBlocks(data, spriteName, commentDatas):
    mutationDatas = {}
    for j, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    additionalBlockDatas = {}
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_call":
                customOpcode = blockData["fields"]["customOpcode"]
                del blockData["fields"]["customOpcode"]
                proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
                mutationData         = mutationDatas[proccode]
                modifiedMutationData = mutationData.copy()
                del modifiedMutationData["argumentnames"]
                del modifiedMutationData["argumentdefaults"]
                blockData["mutation"] = modifiedMutationData
        
                argumentIDs   = json.loads(mutationData["argumentids"])
                argumentNames = json.loads(mutationData["argumentnames"])
                blockData["inputs"] = {
                    argumentIDs[argumentNames.index(inputID)]: 
                    inputValue for j,inputID,inputValue in ikv(blockData["inputs"]) 
                }
            
            if blockData["opcode"] == "control_stop":
                #pp(blockData)
                match blockData["fields"]["STOP_OPTION"][0]:
                    case "all" | "this script"    : hasNext = False
                    case "other scripts in sprite": hasNext = True
                blockData["mutation"] = {
                    "tagName": "mutation",
                    "children": [],
                    "hasnext": json.dumps(hasNext)
                }
    
    
    
    def getSelectors(obj):
        selectors = []
        if isinstance(obj, dict):
            for i,k,v in ikv(obj):
                if isinstance(k, newTempSelector):
                    selectors.append(k)
                if isinstance(v, newTempSelector):
                    selectors.append(v)
                else:
                    selectors += getSelectors(v)
        elif isinstance(obj, list):
            for v in obj:
                if isinstance(v, newTempSelector):
                    selectors.append(v)
                else:
                    selectors += getSelectors(v)
        return selectors
    def replaceSelectors(obj, table):
        if isinstance(obj, dict):
            newObj = {}
            for i,k,v in ikv(obj):
                if isinstance(v, newTempSelector): newV = table[v]
                else                             : newV = replaceSelectors(v, table=table)
                if isinstance(k, newTempSelector): newObj[table[k]] = newV
                else                             : newObj[k] = newV
        elif isinstance(obj, list):
            newObj = []
            for i,v in enumerate(obj):
                if isinstance(v, newTempSelector): newObj.append(table[v])
                else                             : newObj.append(replaceSelectors(v, table=table))
        else:
            newObj = obj
        return newObj
    selectors = getSelectors(data) + getSelectors(commentDatas)
    cutSelectors = []
    for selector in selectors:
        if selector not in cutSelectors:
            cutSelectors.append(selector)
    # Translation table from selector object to literal
    table = {selector: numberToLiteral(i+1) for i,selector in enumerate(cutSelectors)}
    data = replaceSelectors(data, table=table)
    commentDatas = replaceSelectors(commentDatas, table=table)
    return data, commentDatas
