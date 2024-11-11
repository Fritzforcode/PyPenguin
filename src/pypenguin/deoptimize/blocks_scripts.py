import json

from helper_functions import ikv, pp, WhatIsGoingOnError, generateSelector, generateRandomToken, readJSONFile

from deoptimize.options import translateOptions
from deoptimize.comments import translateComment

from database import opcodeDatabase

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

def getCustomBlockInfo(data, spriteNames):
    info = {k:{} for k in spriteNames+[None]}
    for spriteData in data:
        spriteName = None if spriteData["isStage"] else spriteData["name"]
        for scriptData in spriteData["scripts"]:
            firstBlockData = scriptData["blocks"][0]
            if firstBlockData["opcode"] == "define ...":
                customBlockId = firstBlockData["options"]["id"]
                info[spriteName][customBlockId] = generateProccodeFromSegments(firstBlockData["segments"])
    return info
                

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
    if opcode == "special_define":
        newBlockData["segments"] = data["segments"]
    return newBlockData

def linkBlocksToScript(data, spriteName, tokens, scriptIDs):
    if "opcode" not in data:
        scriptPosition = data["position"]
        data = data["blocks"]
    else:
        scriptPosition = None
    newData = {}
    newCommentDatas = {}
    for i, blockData in enumerate(data):
        ownID = generateSelector(scriptIDs=scriptIDs, index=i, isComment=False)
        commentID = generateSelector(scriptIDs=scriptIDs, index=i, isComment=True)
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
            nextID = generateSelector(scriptIDs=scriptIDs, index=i+1, isComment=False)
            newBlockData["next"] = nextID
        if i - 1 in range(len(data)):
            parentID = generateSelector(scriptIDs=scriptIDs, index=i-1, isComment=False)
            newBlockData["parent"] = parentID
        newData[ownID] = newBlockData
                
        commentData = blockData["comment"]
        if commentData != None:
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=ownID,
            )
    return newData, newCommentDatas

def unnestScript(data, spriteName, tokens, scriptIDs):
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
                        case "boolean"    : pass
                        case "instruction": pass
                    if "blocks" in inputData:
                        scriptData = {"position": [0,0], "blocks": inputData["blocks"]}
                        newScriptIDs = scriptIDs + [i] + [j]
                        linkedScriptData, scriptCommentDatasA = linkBlocksToScript(
                            data=scriptData,
                            spriteName=spriteName,
                            tokens=tokens,
                            scriptIDs=newScriptIDs,
                        )
                        unnestedScriptData, scriptCommentDatasB = unnestScript(
                            data=linkedScriptData,
                            spriteName=spriteName,
                            tokens=tokens,
                            scriptIDs=newScriptIDs,
                        )
                        newCommentDatas |= scriptCommentDatasA | scriptCommentDatasB
                        for i,subBlockID,subBlockData in ikv(unnestedScriptData):
                            if "x" in subBlockData:
                                del subBlockData["x"]
                                del subBlockData["y"]
                                subBlockData["parent"] = blockID
                                subBlockData["topLevel"] = False
                            break
                        newBlockDatas |= unnestedScriptData
                        newInputData = [2, subBlockID]
                    elif inputData["block"] == None:
                        if inputData["mode"] == "block-and-text":
                            newInputData = [1, [magicNumber, inputData["text"]]]
                        elif inputData["mode"] == "block-only":
                            newInputData = None
                    else:
                        newBlockID   = generateSelector(scriptIDs=scriptIDs, index=blockCounter, isComment=False)
                        newCommentID = generateSelector(scriptIDs=scriptIDs, index=blockCounter, isComment=True)
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

                if newInputData != None:
                    newInputDatas[inputID] = newInputData
            blockData["inputs"] = newInputDatas

            newBlockDatas[blockID] = blockData
        data = newBlockDatas
        finished = blockCounter == previousBlockCount
        previousBlockCount = blockCounter
    dataCopy = data.copy()
    for i, blockID, blockData in ikv(dataCopy):
        if   blockData["opcode"] == "special_define":
            proccode = generateProccodeFromSegments(blockData["segments"])
            blockCounter = 2
            argumentIDs      = []
            argumentNames    = []
            argumentDefaults = []
            argumentBlockIDs = []
            for segment in blockData["segments"]:
                if   segment["type"] == "label":
                    pass
                elif segment["type"] == "textInput":
                    argumentIDs     .append( generateRandomToken() )
                    argumentNames   .append( segment["name"] )
                    argumentDefaults.append( "" )
                    argumentBlockIDs.append( generateSelector(blockID, blockCounter, False) )
                    blockCounter += 1
                elif segment["type"] == "booleanInput":
                    argumentIDs     .append( generateRandomToken() )
                    argumentNames   .append( segment["name"] )
                    argumentDefaults.append( False )
                    argumentBlockIDs.append( generateSelector(blockID, blockCounter, False) )
            
            match blockData["fields"]["blockType"]:
                case "instruction"    : returns, optype, opcode = False, "statement", "procedures_definition"
                case "lastInstruction": returns, optype, opcode = None , "end"      , "procedures_definition"
                case "stringReporter" : returns, optype, opcode = True , "string"   , "procedures_definition_return" 
                case "numberReporter" : returns, optype, opcode = True , "number"   , "procedures_definition_return"
                case "booleanReporter": returns, optype, opcode = True , "boolean"  , "procedures_definition_return"
            
            definitionID = blockID
            prototypeID = generateSelector(blockID, 1, False)
            definitionData = {
                "opcode": opcode,
                "next": blockData["next"],
                "parent": None,
                "inputs": {"custom_block": [1, prototypeID]},
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": blockData["x"],
                "y": blockData["y"],
            }
            prototypeData = {
                "opcode"  : "procedures_prototype",
                "next"    : None,
                "parent"  : definitionID,
                "inputs"  : { argumentIDs[j]: [1, argumentBlockIDs[j]] for j in range(len(argumentIDs)) }, 
                "fields"  : {},
                "shadow"  : True,
                "topLevel": False,
                "mutation": {
                    "tagName"         : "mutation",
                    "children"        : [],
                    "proccode"        : proccode,
                    "argumentids"     : json.dumps(argumentIDs),
                    "argumentnames"   : json.dumps(argumentNames),
                    "argumentdefaults": json.dumps(argumentDefaults),
                    "warp"            : json.dumps(blockData["fields"]["noScreenRefresh"]),
                    "returns"         : json.dumps(returns),
                    "edited"          : json.dumps(True),
                    "optype"          : json.dumps(optype),
                    "color"           : json.dumps(["#FF6680", "#eb3d5b", "#df2847"]),
                }
            }
            data[definitionID] = definitionData
            data[prototypeID] = prototypeData
            for j in range(len(argumentIDs)):
                data[argumentBlockIDs[j]] = {
                    "opcode": "argument_reporter_string_number" if argumentDefaults[j] == "" else "argument_reporter_boolean",
                    "next": None,
                    "parent": prototypeID,
                    "inputs": {},
                    "fields": {
                        "VALUE": [argumentNames[j], generateRandomToken()]
                    },
                    "shadow": True,
                    "topLevel": False,
                    "mutation": {
                        "tagName": "mutation",
                        "children": [],
                        "color": "[\"#FF6680\",\"#eb3d5b\",\"#df2847\"]"
                    }
                }
        elif blockData["opcode"] in ["special_variable_value", "special_list_value"]:
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

def finishBlocks(data, spriteName, tokens):
    mutationDatas = {}
    for j, blockID, blockData in ikv(data):
        if blockData["opcode"] == "procedures_prototype":
            mutationData = blockData["mutation"]
            mutationDatas[mutationData["proccode"]] = mutationData
    customBlockInfo = tokens["customBlocks"]
    for i, blockID, blockData in ikv(data):
        if blockData["opcode"] == "procedures_call":
            customBlockId = blockData["fields"]["blockDef"]
            proccode = customBlockInfo[spriteName][customBlockId]
            mutationData = mutationDatas[proccode].copy()
            del mutationData["argumentnames"]
            del mutationData["argumentdefaults"]
            blockData["mutation"] = mutationDatas[proccode]
            del blockData["fields"]["blockDef"]
    
    return data
