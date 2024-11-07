from helper_functions import ikv, pp, WhatIsGoingOnError, generateSelector, readJSONFile

from deoptimize.options import translateOptions
from deoptimize.comments import translateComment

from database import opcodeDatabase

def prepareBlock(data, spriteName, tokens, commentID):
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

def linkBlocksToScript(data, spriteName, tokens, scriptID):
    if "opcode" not in data:
        scriptPosition = data["position"]
        data = data["blocks"]
    else:
        scriptPosition = None
    newData = {}
    newCommentDatas = {}
    for i, blockData in enumerate(data):
        ownID = generateSelector(scriptID=scriptID, index=i, isComment=False)
        commentID = generateSelector(scriptID=scriptID, index=i, isComment=True)
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
            nextID = generateSelector(scriptID=scriptID, index=i+1, isComment=False)
            newBlockData["next"] = nextID
        if i - 1 in range(len(data)):
            parentID = generateSelector(scriptID=scriptID, index=i-1, isComment=True)
            newBlockData["parent"] = parentID
        newData[ownID] = newBlockData
                
        commentData = blockData["comment"]
        if commentData != None:
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=ownID,
            )
            
    return newData, newCommentDatas

def unnestScript(data, spriteName, tokens, scriptID):
    previousBlockCount = 0
    blockCounter = len(data)
    finished = False
    newCommentDatas = {}
    while not finished:
        newBlockDatas = {}
        for i,blockID,blockData in ikv(data):
            opcodeData = opcodeDatabase[blockData["opcode"]]
            newInputDatas = {}
            for j,inputID,inputData in ikv(blockData["inputs"]):
                if isinstance(inputData, dict):
                    match opcodeData["inputTypes"][inputID]:
                        case "broadcast"  : magicNumber = 11
                        case "text"       : magicNumber = 10
                        case "number"     : magicNumber =  4
                        case "boolean"    : magicNumber =  2
                        case "instruction": magicNumber =  2
                    if inputData["block"] == None:
                        if inputData["mode"] == "block-and-text":
                            newInputData = [1, [magicNumber, inputData["text"]]]
                        elif inputData["mode"] == "block-only":
                            newInputData = None
                    else:
                        newBlockID = generateSelector(scriptID=scriptID, index=blockCounter, isComment=False)
                        newCommentID = generateSelector(scriptID=scriptID, index=blockCounter, isComment=True)
                        newBlockData = prepareBlock(
                            data=inputData["block"],
                            spriteName=spriteName,
                            tokens=tokens,
                            commentID=newCommentID,
                        )
                        newBlockData["parent"] = blockID
                        blockCounter += 1
                        newBlockDatas[newBlockID] = newBlockData
                        
                        commentData = inputData["block"]["comment"]
                        if commentData != None:
                            newCommentDatas[newCommentID] = translateComment(
                                data=commentData,
                                id=newBlockID,
                            )
                        if inputData["mode"] == "block-and-text":
                            newInputData = [3, newBlockID, [magicNumber, inputData["text"]]]
                        elif inputData["mode"] == "block-only":
                            newInputData = [2, newBlockID]
                else:
                    newInputData = inputData


                newInputDatas[inputID] = newInputData
            blockData["inputs"] = newInputDatas


            newBlockDatas[blockID] = blockData
        data = newBlockDatas
        finished = blockCounter == previousBlockCount
        previousBlockCount = blockCounter
    dataCopy = data.copy()
    for i, blockID, blockData in ikv(dataCopy):
        if blockData["opcode"] in ["special_variable_value", "special_list_value"]:
            if   blockData["opcode"] == "special_variable_value": magicNumber = 12; key = "VARIABLE"
            elif blockData["opcode"] == "special_list_value":     magicNumber = 13; key = "LIST"
            core = [magicNumber, blockData["fields"][key][0], blockData["fields"][key][1]]
            if blockData["parent"] == None: # If the block is independent
                data[blockID] = core + [blockData["x"], blockData["y"]]
            else:
                parentBlockData = data[blockData["parent"]]
                for j, inputID, inputData in ikv(parentBlockData["inputs"]):
                    if inputData[1] == blockID:
                        data[blockData["parent"]]["inputs"][inputID][1] = core
                del data[blockID]
    return data, newCommentDatas
