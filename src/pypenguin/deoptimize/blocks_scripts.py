import json, copy

from pypenguin.helper_functions import ikv, pp, WhatIsGoingOnError, numberToLiteral, newTempSelector, generateRandomToken, parseCustomOpcode
from pypenguin.deoptimize.options import translateOptions
from pypenguin.deoptimize.comments import translateComment
from pypenguin.database import *#opcodeDatabase, inputDefault, optionDefault, commentDefault, inputModes, inputBlockDefault, inputTextDefault, inputBlocksDefault, getInputMode, getInputType, getMenu, getInputMagicNumber, getDeoptimizedOpcode


def unfinishScripts(data):
    newScriptDatas = []
    for scriptData in data:
        newBlockDatas = []
        for i, blockData in enumerate(scriptData["blocks"]):
            newBlockDatas.append(unfinishBlock(
                data=blockData,
                position=scriptData["position"] if i == 0 else None
            ))
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks"  : newBlockDatas,
        })
    return newScriptDatas

def unfinishBlock(data, position=None):
    #print("start fblock", 100*"{")
    #pp(data)
    blockType = getBlockType(
        opcode=getDeoptimizedOpcode(
            opcode=data["opcode"]
        ),
    )
    if blockType == "menu":
        raise NotImplementedError("YET TO BE IMPLEMENTED")
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
            newInputData["block"]  = unfinishBlock(data=inputData["block"])
        if inputData.get("blocks") != None:
            newInputData["blocks"] = [unfinishBlock(data=subBlockData) for subBlockData in inputData["blocks"]]
        if inputData.get("option") != None:
            newInputData["option"] = unfinishBlock(data=inputData["option"])
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
        blockIDs = [newTempSelector() for i in range(len(scriptData["blocks"]))]
        for i, blockData in enumerate(scriptData["blocks"]):
            blockID = blockIDs[i]
            if i - 1 in range(len(scriptData["blocks"])): # When the block has a upwards neighbour
                parentID = blockIDs[i - 1]
            else:
                parentID = None
            if i + 1 in range(len(scriptData["blocks"])): # When the block has a downwards neighbour
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
                    nextID=None
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
    return newBlockDatas

def unprepareBlocks(data):
    pp(data)
    newBlockDatas = {}
    for i, blockID, blockData in ikv(data):
        opcode = getDeoptimizedOpcode(opcode=blockData["opcode"])

        newBlockData = {
            "opcode"  : opcode,
            "next"    : blockData["_info_"]["next"],
            "parent"  : blockData["_info_"]["parent"],
            "inputs"  : unprepareInputs(
                data=blockData["inputs"],
                opcode=opcode,
            ),
            "fields"  : unprepareOptions(
                data=blockData["options"],
                opcode=opcode,
            ),
            "shadow"  : False,
            "topLevel": blockData["_info_"]["topLevel"],
        }
        if blockData["_info_"]["position"] != None:
            position = blockData["_info_"]["position"]
            newBlockData |= {"x": position[0], "y": position[1]}

def unprepareInputs(data, opcode):
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
        #TODO: translate input values
        print(inputID, inputType, inputMode)
    return newInputDatas

def unprepareOptions(data, opcode):
    return data
