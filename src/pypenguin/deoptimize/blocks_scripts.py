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
    if opcode in ["special_variable_value", "special_list_value"]:
        if opcode == "special_variable_value":
            magicValue = 12
            name = data["options"]["VARIABLE"]
            if name in tokens["variables"][spriteName]:
                token = tokens["variables"][spriteName][name]
            elif name in tokens["variables"][None]:
                token = tokens["variables"][None][name]
        elif opcode == "special_list_value":
            magicValue = 13
            name = data["options"]["LIST"]
            if name in tokens["lists"][spriteName]:
                token = tokens["lists"][spriteName][name]
            elif name in tokens["lists"][None]:
                token = tokens["lists"][None][name]
        newBlockData = [
            magicValue,
            name,
            token,
        ]
    else:
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
        if isinstance(newBlockData, dict):
            if i == 0:
                newBlockData |= {"x": scriptPosition[0], "y": scriptPosition[1]}
                newBlockData["topLevel"] = True
            if i + 1 in range(len(data)):
                nextID = generateSelector(scriptID=scriptID, index=i+1, isComment=False)
                newBlockData["next"] = nextID
            if i - 1 in range(len(data)):
                parentID = generateSelector(scriptID=scriptID, index=i-1, isComment=True)
                newBlockData["parent"] = parentID
        elif isinstance(newBlockData, list):
            pp(blockData)
            newBlockData += scriptPosition

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
            if isinstance(blockData, list):
                if   blockData[0] == 12: opcode = "special_variable_value"
                elif blockData[1] == 13: opcode = "special_list_value"
            else:
                opcode = blockData["opcode"]
            opcodeData = opcodeDatabase[opcode]
            newInputDatas = {}
            for j,inputID,inputData in ikv(blockData["inputs"]):
                #if isinstance(inputData, dict):
                match opcodeData["inputTypes"][inputID]:
                    case "broadcast": magicNumber = 11
                    case "text"     : magicNumber = 10
                    case "number"   : magicNumber =  4
                    case "boolean"  : magicNumber =  2
                if isinstance(inputData, list) or inputData["mode"] == "block-and-text":
                    if isinstance(inputData, dict):
                        if inputData["block"] == None: hasBlock = False
                        else: hasBlock = True
                    else: hasBlock = True
                    if not hasBlock:
                        newInputData = [1, [magicNumber, inputData["text"]]]
                    else:
                        newBlockID = generateSelector(scriptID=scriptID, index=blockCounter, isComment=False)
                        newCommentID = generateSelector(scriptID=scriptID, index=blockCounter, isComment=True)
                        newBlockData = prepareBlock(
                            data=inputData["block"],
                            spriteName=spriteName,
                            tokens=tokens,
                            commentID=newCommentID,
                        )
                        if isinstance(newBlockData, list):
                            newBlockID = newBlockData
                        elif isinstance(newBlockData, dict):
                            newBlockData["parent"] = blockID
                            blockCounter += 1
                            newBlockDatas[newBlockID] = newBlockData
                        
                            commentData = inputData["block"]["comment"]
                            if commentData != None:
                                newCommentDatas[newCommentID] = translateComment(
                                    data=commentData,
                                    id=newBlockID,
                                )
                        newInputData = [3, newBlockID, [magicNumber, inputData["text"]]]
                else:
                    raise WhatIsGoingOnError(inputData)
                #else:
                #    newInputData = inputData
                newInputDatas[inputID] = newInputData
            blockData["inputs"] = newInputDatas
            print("x")
            pp(blockData)
            newBlockDatas[blockID] = blockData
        data = newBlockDatas
        finished = blockCounter == previousBlockCount
        previousBlockCount = blockCounter

    return data, newCommentDatas
