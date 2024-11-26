
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
    
    opcode = getDeoptimizedOpcode(opcode=data["opcode"])
    
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

def linkBlocksToScript(data, spriteName, tokens):
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

def autoCompleteInput(data, opcode, inputID):
    # Add properties that are not defined and set them to their defaults.
    inputMode = getInputMode(
        opcode=opcode,
        inputID=inputID,
    )
    newData = {
        "mode": inputMode,
    }
    
    if   inputMode == "block-and-text":
        required = ["block", "text"]
    elif inputMode == "block-only":
        required = ["block"]
    elif inputMode == "block-and-option":
        required = ["block", "option"]
    elif inputMode == "script":
        required = ["blocks"]
    
    for attribute in required:
        if attribute in data:
            newData[attribute] = data[attribute]
        else:
            match attribute:
                case "block":
                    newData["block"] = inputBlockDefault
                case "text":
                    newData["text"] = inputTextDefault
                case "blocks":
                    newData["blocks"] = inputBlocksDefault
                case "option":
                    raise Exception()
    return newData

def unnestScript(data, spriteName, tokens):
    print(100*"(")
    pp(data)
    newBlockDatas = {}
    newCommentDatas = {}
    
    for i, blockID, blockData in ikv(data):
        opcode = blockData["opcode"]
        for j, inputID, inputData in ikv(blockData["inputs"]):
            inputType = getInputType(
                opcode=opcode,
                inputID=inputID,
            )
            
            print("-", inputID, inputData)
            menuID     = newTempSelector()
            subBlockID = newTempSelector()
            inputData = autoCompleteInput(
                data=inputData,
                opcode=opcode,
                inputID=inputID,
            )
            
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
                #additionalBlockDatas[menuID] = menuBlockData
                #blockData["inputs"][outerID] = [1, menuID]
            
            if inputData.get("block") != None:
                subBlockData = prepareBlock(
                    
                )
                temp = unnestScript(
                    data={subBlockID: inputData["block"]},
                    spriteName=spriteName,
                    tokens=tokens,
                )
                newBlockDatas   |= temp[0]
                newCommentDatas |= temp[1]
                print(getInputMagicNumber(inputType))
    
    pp(newBlockDatas)
    print(100*")")
    return newBlockDatas, {} # nothing for comments temporarily

def finishBlocks(*a, **b):
    return (1,2)