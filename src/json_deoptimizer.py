from helper_functions import ikv, pp, readJSONFile, writeJSONFile, generateRandomToken, flipKeysAndValues, generateSelector, WhatIsGoingOnError

opcodeDatabase = readJSONFile("opcode_database.jsonc")

def translateVariables(data, spriteNames):
    tokens = {k:{} for k in spriteNames+[None]}
    newData = {k:{} for k in spriteNames+[None]}
    #print(Tokens)
    #print(newData)
    for variableData in data:
        sprite = variableData["sprite"]
        name = variableData["name"]
        tokens[sprite][name] = generateRandomToken()


        newVariableData = [name, variableData["currentValue"]]
        match variableData["mode"]:
            case "cloud":
                if not name.startswith("\u2601 "): raise ValueError("Cloud variables have to start with '☁ ' eg. '☁ var'")
            case "global":
                if "\u2601" in name: raise ValueError("Non-cloud variables cannot contain '☁'")
            case "local":
                if "\u2601" in name: raise ValueError("Non-cloud variables cannot contain '☁'")
            case _: raise WhatIsGoingOnError()
            

        newData[sprite][tokens[sprite][name]] = newVariableData
    return newData, tokens

def translateLists(data, spriteNames):
    tokens = {k:{} for k in spriteNames+[None]}
    newData = {k:{} for k in spriteNames+[None]}
    #print(Tokens)
    #print(newData)
    for listData in data:
        sprite = listData["sprite"]
        name = listData["name"]
        tokens[sprite][name] = generateRandomToken()


        newListData = [name, listData["currentValue"]]
        newData[sprite][tokens[sprite][name]] = newListData
    return newData, tokens

def findBlockBroadcastMessages(data):
    for i,opcode,opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == data["opcode"]:
            break
    if not opcodeData["newOpcode"] == data["opcode"]: raise WhatIsGoingOnError(data["opcode"])
    
    broadcastMessages = []
    for i,inputID,inputData in  ikv(data["inputs"]):
        #print("in", inputID, inputData["text"], opcodeData["inputTypes"])
        #print(opcodeData["inputTypes"][inputID])
        if opcodeData["inputTypes"][inputID] == "broadcast":
            if inputData["text"] not in broadcastMessages:
                broadcastMessages.append(inputData["text"])
        
        if "block" in inputData:
            if inputData["block"] != None:
                broadcastMessages += findBlockBroadcastMessages(data=inputData["block"])
    for i,optionID,optionData in  ikv(data["options"]):
        #print("opt", optionID, optionData, opcodeData["optionTypes"])
        #print(opcodeData["optionTypes"][optionID])
        if opcodeData["optionTypes"][optionID] == "broadcast":
            if optionData not in broadcastMessages:
                broadcastMessages.append(optionData)
    return broadcastMessages
    

def generateBroadcastTokens(data, spriteNames):
    broadcastMessages = []
    for spriteData in data:
        for scriptData in spriteData["scripts"]:
            for blockData in scriptData["blocks"]:
                #pp(blockData)
                broadcastMessages += findBlockBroadcastMessages(data=blockData)
    broadcastMessages = dict.fromkeys(broadcastMessages).keys() # Remove duplicates
    tokens = {}
    for broadcastMessage in broadcastMessages:
        tokens[broadcastMessage] = generateRandomToken()
    # Because all broadcast messages are for all sprites (None=Stage)
    newTokens = {spriteName:{} for spriteName in spriteNames}
    newTokens[None] = tokens 
    return newTokens


def translateOptions(optionDatas, opcode, spriteName, tokens):
    variableTokens = tokens["variables"]
    listTokens = tokens["lists"]
    broadcastTokens = tokens["broadcasts"]
    
    #print("- toptions")
    #print(optionDatas)
    #print(variableTokens)
    #print(broadcastTokens)
    newData = {}
    opcodeData = opcodeDatabase[opcode]
    for i,optionID,optionData in ikv(optionDatas):
        #print("||", optionID, optionData)
        mode = opcodeData["optionTypes"][optionID]
        if mode == "variable" or mode == "list" or mode == "broadcast":
            if mode == "variable":
                tokens = variableTokens
                magicString = ""
            elif mode == "list":
                tokens = listTokens
                magicString = "list"
            elif mode == "broadcast":
                tokens = broadcastTokens
                magicString = "broadcast_msg"
            
            if spriteName not in tokens:
                if spriteName == "Stage":
                    nameKey = None
                else: raise Exception()
            elif optionData in variableTokens[spriteName]:
                nameKey = spriteName
            else:
                nameKey = None
            token = tokens[nameKey][optionData]
            newOptionData = [optionData, token, magicString]
        elif mode == "pressed key":
            newOptionData = [optionData, generateRandomToken()]
        else: raise WhatIsGoingOnError()
        newData[optionID] = newOptionData
    return newData

def prepareBlock(data, spriteName, tokens):
    #print("- prep")
    #pp(data)
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

def translateComment(data, id):
    return {
        "blockId"  : id,
        "x"        : data["position"][0],
        "y"        : data["position"][1],
        "width"    : data["size"][0],
        "height"   : data["size"][1],
        "minimized": data["minimized"],
        "text"     : data["text"],
    }

def linkBlocksToScript(data, spriteName, tokens, scriptID):
    #print(222*"-")
    #pp(broadcastDatas)
    if "opcode" not in data:
        scriptPosition = data["position"]
        data = data["blocks"]
    else:
        scriptPosition = None
    newData = {}
    newCommentDatas = {}
    for i, blockData in enumerate(data):
        #pp(blockData)
        newBlockData = prepareBlock(
            data=blockData, 
            spriteName=spriteName, 
            tokens=tokens,
        )
        #pp(newBlockData)
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
        #print(888*"!")
        #print("new iter")
        #pp(data)
        #print(888*":")
        newBlockDatas = {}
        for i,blockID,blockData in ikv(data):
            #print(blockID, 439*"$")
            #pp(blockData)
            opcodeData = opcodeDatabase[blockData["opcode"]]
            newInputDatas = {}
            for j,inputID,inputData in ikv(blockData["inputs"]):
                #print(j, 220*"-")
                #pp(inputData)
                if isinstance(inputData, dict):
                    #print(opcodeData)
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
                                #pp(newBlockData)
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
        #pp(newBlockDatas)
        data = newBlockDatas
        finished = blockCounter == previousBlockCount
        previousBlockCount = blockCounter

    #pp(data)
    return data, newCommentDatas

def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        pp(costumeData)
        newCostumeData = {
            "name"            : costumeData["name"],
            "bitmapResolution": None,
            "assetId"         : costumeData["fileStem"],
            "dataFormat"      : costumeData["dataFormat"],
            "md5ext"          : costumeData["fileStem"] + "." + costumeData["dataFormat"],
            "rotationCenterX" : costumeData["rotationCenter"][0],
            "rotationCenterY" : costumeData["rotationCenter"][1],
        }
        if "bitmapResolution" in costumeData:
            newCostumeData["bitmapResolution"] = costumeData["bitmapResolution"]
        else:
            del newCostumeData["bitmapResolution"]
        newCostumeDatas.append(newCostumeData)
    return newCostumeDatas

def translateSounds(data):
    newSoundDatas = []
    for soundData in data:
        newSoundData = {
            "name"       : soundData["name"],
            "assetId"    : soundData["fileStem"],
            "dataFormat" : soundData["dataFormat"],
            "rate"       : soundData["rate"],        # playback speed in Hz
            "sampleCount": soundData["sampleCount"], # = "rate" * duration in secs
            "md5ext"     : soundData["fileStem"] + "." + soundData["dataFormat"],
        }
        newSoundDatas.append(newSoundData)
    return newSoundDatas

def deoptimizeProject(sourcePath, targetPath):
    data = readJSONFile(sourcePath)
    spriteNames = [sprite["name"] for sprite in data["sprites"]][1:]
    ##pp(data["variables"])
    translatedVariableDatas, variableTokens = translateVariables(
        data=data["variables"], 
        spriteNames=spriteNames,
    )
    translatedListDatas, listTokens = translateLists(
        data=data["lists"], 
        spriteNames=spriteNames,
    )
    #pp(translatedListDatas)
    broadcastTokens = generateBroadcastTokens(
        data=data["sprites"],
        spriteNames=spriteNames,
    )
    tokens = {
        "variables" : variableTokens,
        "lists"     : listTokens,
        "broadcasts": broadcastTokens,
    }
    #pp(tokens)
    
    #pp(data["lists"])
    #pp(translatedListDatas)
    #pp(listTokens)
    
    
    #pp(translatedVariableDatas)
    newSpriteDatas = []
    for spriteData in data["sprites"]:
        newCommentDatas = {}
        #print(spriteData.keys())
        #commentDatas = spriteData["comments"]
        newSpriteBlocks = {}
        #pp(spriteData)
        for scriptID, scriptData in enumerate(spriteData["scripts"]):
            print(444*"|")
            pp(scriptData)
            linkedScriptData, scriptCommentDatasA = linkBlocksToScript(
                data=scriptData, 
                spriteName=spriteData["name"],
                tokens=tokens,
                scriptID=scriptID,
            )
            
            unnestedScriptData, scriptCommentDatasB = unnestScript(
                data=linkedScriptData, 
                spriteName=spriteData["name"],
                tokens=tokens,
                scriptID=scriptID,
            )
            scriptCommentDatas = scriptCommentDatasA | scriptCommentDatasB
            newCommentDatas |= scriptCommentDatas
            pp(scriptCommentDatas)
            #pp(unnestedScriptData)
            newSpriteBlocks |= unnestedScriptData
        nameKey = None if spriteData["isStage"] else spriteData["name"]
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = generateSelector(scriptID=None, index=i, isComment=True)
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=None,
            )
        
        newCostumeDatas = translateCostumes(
            data=spriteData["costumes"],
        )
        newSoundDatas = translateSounds(
            data=spriteData["sounds"],
        )
        
        
        newSpriteData = {
            "isStage"       : spriteData["isStage"],
            "name"          : spriteData["name"],
            "variables"     : translatedVariableDatas[nameKey],
            "lists"         : translatedListDatas    [nameKey],
            "broadcasts"    : {},
            "customVars"    : [], # NO MEANING FOUND
            "blocks"        : newSpriteBlocks,
            "comments"      : newCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : newCostumeDatas,
            "sounds"        : newSoundDatas,
            "id"            : generateRandomToken(),
            "volume"        : spriteData["volume"],
            "layerOrder"    : spriteData["layerOrder"],
        }
        if spriteData["isStage"]:
            newSpriteData["broadcasts"] = flipKeysAndValues(broadcastTokens[None])
            newSpriteData |= {
                "tempo"               : spriteData["tempo"],
                "videoTransparency"   : spriteData["videoTransparency"],
                "videoState"          : spriteData["videoState"],
                "textToSpeechLanguage": spriteData["textToSpeechLanguage"],
            }
        else:
            newSpriteData |= {
                "visible"      : spriteData["visible"],
                "x"            : spriteData["position"][0],
                "y"            : spriteData["position"][1],
                "size"         : spriteData["size"],
                "direction"    : spriteData["direction"],
                "draggable"    : spriteData["draggable"],
                "rotationStyle": spriteData["rotationStyle"],
            }
        newSpriteDatas.append(newSpriteData)
    newProjectData = {
        "targets"      : newSpriteDatas,
        "monitors"     : data["monitors"],
        "extensionData": data["extensionData"],
        "extensions"   : data["extensions"],
        "meta"         : data["meta"],
    }
    pp(newProjectData)
    writeJSONFile(targetPath, newProjectData)    


deoptimizeProject(sourcePath="optimized.json", targetPath="deoptimized.json")
