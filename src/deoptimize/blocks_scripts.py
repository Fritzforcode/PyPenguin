from helper_functions import ikv, WhatIsGoingOnError, generateSelector, readJSONFile
from options import translateOptions
from comments import translateComment

opcodeDatabase = readJSONFile("assets/opcode_database.jsonc")


def prepareBlock(data, spriteName, tokens):
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
        newBlockData = prepareBlock(
            data=blockData, 
            spriteName=spriteName, 
            tokens=tokens,
        )
        ownID = generateSelector(scriptID=scriptID, index=i, isComment=False)
        commentID = generateSelector(scriptID=scriptID, index=i, isComment=True)
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
                        case "broadcast": magicNumber = 11
                        case "text"     : magicNumber = 10
                        case "number"   : magicNumber =  4
                        case "boolean"  : magicNumber =  2
                    match inputData["mode"]:
                        case "block-and-text":
                            if inputData["block"] == None:
                                newInputData = [1, [magicNumber, inputData["text"]]]
                            else:
                                newBlockData = prepareBlock(
                                    data=inputData["block"],
                                    spriteName=spriteName,
                                    tokens=tokens,
                                )
                                newBlockData["parent"] = blockID
                                newBlockID = generateSelector(scriptID=scriptID, index=blockCounter, isComment=False)
                                newCommentID = generateSelector(scriptID=scriptID, index=blockCounter, isComment=True)
                                blockCounter += 1
                                newBlockDatas[newBlockID] = newBlockData
                                
                                commentData = inputData["block"]["comment"]
                                if commentData != None:
                                    newCommentDatas[newCommentID] = translateComment(
                                        data=commentData,
                                        id=newBlockID,
                                    )
                                newInputData = [3, newBlockID, [magicNumber, inputData["text"]]]
                        case _:
                            raise WhatIsGoingOnError(inputData)
                else:
                    newInputData = inputData
                newInputDatas[inputID] = newInputData
            blockData["inputs"] = newInputDatas
            newBlockDatas[blockID] = blockData
        data = newBlockDatas
        finished = blockCounter == previousBlockCount
        previousBlockCount = blockCounter

    return data, newCommentDatas
