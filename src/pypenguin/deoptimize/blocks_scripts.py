import json, copy

from pypenguin.helper_functions import ikv, pp, WhatIsGoingOnError, numberToLiteral, newTempSelector, generateRandomToken, parseCustomOpcode
from pypenguin.deoptimize.options import translateOptions
from pypenguin.deoptimize.comments import translateComment
from pypenguin.database import opcodeDatabase, inputDefault, optionDefault, commentDefault, inputModes, inputBlockDefault, inputTextDefault, inputBlocksDefault, getInputMode, getMenu


def generateProccodeFromSegments(data):
    proccode = ""
    for segment in data:
        if   segment["type"] == "label":
            if proccode != "": proccode += " "
            proccode += segment["text"]
        elif segment["type"] == "textInput":
            proccode += " %s"
        elif segment["type"] == "booleanInput":
            proccode += " %b"
    return proccode

def prepareBlock(data, spriteName, tokens, commentID):
    if "inputs" not in data:
        data["inputs"] = inputDefault
    if "options" not in data:
        data["options"] = optionDefault
    if "comment" not in data:
        data["comment"] = commentDefault
    
    opcode = None
    for i,oldOpcode,opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == data["opcode"]:
            opcode = oldOpcode
    if opcode == None:
        raise WhatIsGoingOnError(data["opcode"])
    
    newBlockData = {
        "opcode"  : opcode,
        "next"    : None,
        "parent"  : None,
        "inputs"  : data["inputs"],
        "fields"  : translateOptions(
            optionDatas=data["options"], 
            opcode=opcode, 
            spriteName=spriteName,
            tokens=tokens,
        ),
        "shadow"  : False,
        "topLevel": False,
    }
    if data["comment"] != None:
        newBlockData["comment"] = commentID
    return newBlockData

def linkBlocksToScript(data, spriteName, tokens, scriptIDs):
    if "opcode" not in data:
        scriptPosition = data["position"]
        data = data["blocks"]
    else:
        scriptPosition = None
    
    IDs = [newTempSelector() for i in range(len(data))]
    newData = {}
    newCommentDatas = {}
    for i, blockData in enumerate(data):
        ownID = IDs[i]
        commentID = newTempSelector()
        newBlockData = prepareBlock(
            data=blockData, 
            spriteName=spriteName, 
            tokens=tokens,
            commentID=commentID,
        )
        if i == 0:
            newBlockData |= {"x": scriptPosition[0], "y": scriptPosition[1]}
            newBlockData["topLevel"] = True
        if i + 1 in range(len(data)):
            nextID = IDs[i + 1]
            newBlockData["next"] = nextID
        if i - 1 in range(len(data)):
            parentID = IDs[i - 1]
            newBlockData["parent"] = parentID
        newData[ownID] = newBlockData
                
        commentData = blockData["comment"]
        if commentData != None:
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=ownID,
            )
    return newData, newCommentDatas

def unnestScript(data):
    print(100*"(")
    pp(data)
    additionalBlockDatas = {}
    for i, blockID, blockData in ikv(data):
        opcode = blockData["opcode"]
        for j, inputID, inputData in ikv(blockData["inputs"]):
            print("-", inputID, inputData)
            if "option" in inputData:
                menuData = getMenu(
                    opcode=opcode,
                    inputID=inputID,
                )
                if menuData == None: raise Exception("no menu for option found")
                outerID    = menuData["outer"]
                innerID    = menuData["inner"]
                menuOpcode = menuData["menuOpcode"]

                menuValue  = inputData["option"]
                menuID     = newTempSelector()

                menuBlockData = {
                    "opcode": menuOpcode,
                    "next"  : None,
                    "parent": blockID,
                    "inputs": {},
                    "fields": {
                        innerID: menuValue,
                    },
                    "shadow"  : True,
                    "topLevel": False,
                    "_info_": {"isDone": True},
                }
                additionalBlockDatas[menuID] = menuBlockData
                #blockData["inputs"][outerID] = [1, menuID]
            #TODO: here
    
    newData = data | additionalBlockDatas
    pp(newData)
    print(100*")")
    return newData, {} # nothing for comments temporarily

def finishBlocks(*a, **b):
    return (1,2)