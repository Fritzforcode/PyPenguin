import json

from pypenguin.helper_functions import ikv, pp, WhatIsGoingOnError, numberToLiteral, tempSelector, generateRandomToken, parseCustomOpcode

from pypenguin.deoptimize.options import translateOptions
from pypenguin.deoptimize.comments import translateComment

from pypenguin.database import opcodeDatabase

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
    opcode = None
    for i,oldOpcode,opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == data["opcode"]:
            opcode = oldOpcode
    if opcode == None:
        raise WhatIsGoingOnError(data["opcode"])
    
    if "inputs" not in data:
        data["inputs"] = {}
    if "options" not in data:
        data["options"] = {}
    if "comment" not in data:
        data["comment"] = None
    
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
    newData = {}
    newCommentDatas = {}
    for i, blockData in enumerate(data):
        ownID = tempSelector(path=scriptIDs+[i])
        commentID = tempSelector(path=scriptIDs+[i]+["c"])
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
            nextID = tempSelector(path=scriptIDs+[i+1])
            newBlockData["next"] = nextID
        if i - 1 in range(len(data)):
            parentID = tempSelector(path=scriptIDs+[i-1])
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
    def lookupInputMode(opcode, inputID):
        opcodeData = opcodeDatabase[opcode]
        print(opcodeData)
        inputType = opcodeData["inputTypes"][inputID]
        match inputType: # type of the input
            case "broadcast"|"integer"|"positive integer"|"number"|"text":
                inputMode = "block-and-text"
            case "boolean"|"round":
                inputMode = "block-only"
            case "script":
                inputMode = "script"
        return inputMode
        
    previousBlockCount = 0
    blockCounter = len(data)
    finished = False
    newCommentDatas = {}
    while not finished:
        newBlockDatas = {}
        for i,blockID,blockData in ikv(data):
            print(100*"?")
            pp(blockData)
            opcodeData = opcodeDatabase[blockData["opcode"]]
            newInputDatas = {}
            opcode = blockData["opcode"]
            if blockData["opcode"] == "procedures_call":
                customOpcode        = blockData["fields"]["customOpcode"]
                proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
                inputModes = {}
                for i,inputID,inputData in ikv(arguments):
                    if inputData == str:
                        inputModes[inputID] = "block-and-text"
                    elif inputData == bool:
                        inputModes[inputID] = "block-only"
            else:
                inputModes = {inputID: lookupInputMode(opcode, inputID) for inputID in blockData["inputs"]}
            for j,inputID,inputData in ikv(blockData["inputs"]):
                inputMode = inputModes[inputID]
                if isinstance(inputData, dict):
                    if blockData["opcode"] == "procedures_call":
                        if arguments[inputID] == str:
                            magicNumber = 10 # use the value for a text input type
                        elif arguments[inputID] == bool:
                            pass
                    else:
                        match opcodeData["inputTypes"][inputID]:
                            case "broadcast"       : magicNumber = 11
                            case "text"            : magicNumber = 10
                            case "integer"         : magicNumber =  7
                            case "positive integer": magicNumber =  6
                            case "number"          : magicNumber =  4
                            case "boolean"         : pass
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
                        if inputData["blocks"] == []:
                            newInputData = None
                        else:
                            newInputData = [2, subBlockID]
                    elif inputData["block"] == None:
                        if inputMode == "block-and-text":
                            newInputData = [1, [magicNumber, inputData["text"]]]
                        elif inputMode == "block-only":
                            newInputData = None
                    else:
                        newBlockID   = tempSelector(path=scriptIDs+[blockCounter])
                        newCommentID = tempSelector(path=scriptIDs+[blockCounter]+["c"])
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
                        if inputMode == "block-and-text":
                            newInputData = [3, newBlockID, [magicNumber, inputData["text"]]]
                        elif inputMode == "block-only":
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
            customOpcode        = blockData["fields"]["customOpcode"]
            proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
            argumentIDs      = []
            argumentNames    = []
            argumentDefaults = []
            argumentBlockIDs = []
            for i, argumentName, argumentType in ikv(arguments):
                argumentIDs     .append(generateRandomToken())
                argumentNames   .append(argumentName)
                # The argument reporter defaults
                argumentDefaults.append("" if argumentType==str else json.dumps(False))
                argumentBlockIDs.append(
                    tempSelector(path=blockID+[i+2])
                ) # i+2: account for the prototype taking index 1
            
            match blockData["fields"]["blockType"]:
                case "instruction"    : returns, optype, opcode = False, "statement", "procedures_definition"
                case "lastInstruction": returns, optype, opcode = None , "end"      , "procedures_definition"
                case "stringReporter" : returns, optype, opcode = True , "string"   , "procedures_definition_return" 
                case "numberReporter" : returns, optype, opcode = True , "number"   , "procedures_definition_return"
                case "booleanReporter": returns, optype, opcode = True , "boolean"  , "procedures_definition_return"
            
            definitionID = blockID
            prototypeID = tempSelector(path=blockID+[1])
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
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_call":
                customOpcode = blockData["fields"]["customOpcode"]
                del blockData["fields"]["customOpcode"]
                proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
                mutationData = mutationDatas[proccode]
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
            
            opcodeData = opcodeDatabase[blockData["opcode"]]
            if "inputTranslation" in opcodeData:
                # Replace the optmized with the unoptizimzed input ids
                newInputDatas = {}
                newIDs = list(opcodeData["inputTranslation"].keys())
                oldIDs = list(opcodeData["inputTranslation"].values())
                print("odata", opcodeData)
                print(newIDs, oldIDs)
                for j,inputID,inputData in ikv(blockData["inputs"]):
                    newInputID = newIDs[oldIDs.index(inputID)]
                    newInputDatas[newInputID] = inputData
                blockData["inputs"] = newInputDatas
    def getSelectors(obj):
        selectors = []
        if isinstance(obj, dict):
            for i,k,v in ikv(obj):
                if isinstance(k, tempSelector):
                    selectors.append(k)
                if isinstance(v, tempSelector):
                    selectors.append(v)
                else:
                    selectors += getSelectors(v)
        elif isinstance(obj, list):
            for v in obj:
                if isinstance(v, tempSelector):
                    selectors.append(v)
                else:
                    selectors += getSelectors(v)
        return selectors
    def replaceSelectors(obj, table):
        if isinstance(obj, dict):
            newObj = {}
            for i,k,v in ikv(obj):
                if isinstance(v, tempSelector): newV = table[v]
                else                          : newV = replaceSelectors(v, table=table)
                if isinstance(k, tempSelector): newObj[table[k]] = newV
                else                          : newObj[k] = newV
        elif isinstance(obj, list):
            newObj = []
            for i,v in enumerate(obj):
                if isinstance(v, tempSelector): newObj.append(table[v])
                else                          : newObj.append(replaceSelectors(v, table=table))
        else:
            newObj = obj
        return newObj
    selectors = getSelectors(data)
    cutSelectors = []
    for selector in selectors:
        if selector not in cutSelectors:
            cutSelectors.append(selector)
    # Translation table from selector object to literal
    table = {selector: numberToLiteral(i+1) for i,selector in enumerate(cutSelectors)}
    data = replaceSelectors(data, table=table)
    return data
