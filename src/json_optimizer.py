from helper_functions import pp, ikv, readJSONFile, writeJSONFile, WhatIsGoingOnError
print("hi")
opcodeDatabase = readJSONFile("opcode_database.jsonc")

def translateComment(data):
    return {
        "position" : [data["x"], data["y"]],
        "size"     : [data["width"], data["height"]],
        "minimized": data["minimized"],
        "text"     : data["text"],
    }

def processInputs(data):
    newData = {}
    for i,inputID,inputData in ikv(data):
        #print(k,v)
        if len(inputData) == 2:
            if   isinstance(inputData[1], str): # eg. "CONDITION": [2, "b"]
                mode = "block-only"
                pointer = inputData[1]
                text = None
            elif isinstance(inputData[1], list): # eg. "MESSAGE": [1, [10, "Bye!"]]
                mode = "block-and-text"
                pointer = None
                text = inputData[1][1]
            else:
                raise WhatIsGoingOnError(inputData)
        elif len(inputData) == 3:
            if   isinstance(inputData[1], str): # ex 'OPERAND1': [3, 'e', [10, '']]
                mode = "block-and-text"
                pointer = inputData[1]
                text = inputData[2][1]
            else:
                raise WhatIsGoingOnError(inputData)
        else:
            raise WhatIsGoingOnError(inputData)
        if mode == "block-only":
            newInputData = {
                "mode": mode,
                "block": pointer,
            }
        elif mode == "block-and-text":
            newInputData = {
                "mode" : mode,
                "block": pointer,
                "text" : text, 
            }
        else: raise WhatIsGoingOnError()
        newData[inputID] = newInputData
    return newData

def translateOptions(opcode, data):
    #pp(data)
    newData = {}
    for i,fieldID,fieldData in ikv(data):
        opcodeData = opcodeDatabase[opcode]
        #print(opcodeData)
        match opcodeData["optionTypes"][fieldID]:
            case "variable":
                newFieldData = fieldData[0]
            case "list":
                newFieldData = fieldData[0]
            case "broadcast":
                newFieldData = fieldData[0]
            case "pressed key":
                newFieldData = fieldData[0]
            case _: raise WhatIsGoingOnError(opcodeData["optionTypes"][fieldID])
        newData[fieldID] = newFieldData
    return newData

def translateScript(data, ancestorP, blockChildrenPs, commentDatas):
    #print(222*"-")
    childrenDatas = {}
    for pointer in blockChildrenPs[ancestorP]:
        childrenDatas[pointer] = translateScript(
            data=data, 
            ancestorP=pointer, 
            blockChildrenPs=blockChildrenPs,
            commentDatas=commentDatas
        )
    #pp(data)
    #pp(commentDatas)
    blockData = data[ancestorP] # Get the block's own data
    inputs = processInputs(blockData["inputs"])
    for i,inputID,inputData in ikv(inputs):
        if "block" in inputData:
            if inputData["block"] != None:
                inputs[inputID]["block"] = childrenDatas[inputData["block"]][0]
    options = translateOptions(opcode=blockData["opcode"], data=blockData["fields"])
    newOpcode = opcodeDatabase[blockData["opcode"]]["newOpcode"]
    comment = None
    for commentData in commentDatas.values():
        if commentData["blockId"] == ancestorP:
            comment = translateComment(data=commentData)
    newData = {
        "opcode"      : newOpcode,
        "inputs"      : inputs,
        "options"     : options,
        "comment"     : comment,
    }

    newDatas = [newData]
    if blockData["next"] != None: #if the block does not have a neighbour
        newDatas += childrenDatas[blockData["next"]]
    
    #pp(childrenResults)
    #pp(results)
    if blockData["topLevel"] == True:
        return {"position": [blockData["x"], blockData["y"]], "blocks": newDatas} 
    else:
        return newDatas

def translateVariables(data):
    newData = []
    for spriteData in data:
        for i,variableID,variableData in ikv(spriteData["variables"]):
            name = variableData[0]
            currentValue = variableData[1]
            if spriteData["isStage"]:
                if len(variableData) == 3 and variableData[2] == True:
                    mode = "cloud"
                else:
                    mode = "global"
                sprite = None
            else:
                mode = "local"
                sprite = spriteData["name"]
            if spriteData["customVars"] != []:
                raise WhatIsGoingOnError("THANK YOU!!! I have been trying to find out what 'customVars' is used for.")
            newVariableData = {
                "name"        : name,
                "currentValue": currentValue,
                "mode"        : mode,
                "sprite"      : sprite,
            }
            newData.append(newVariableData)
    return newData

def translateLists(data):
    newData = []
    for spriteData in data:
        for i,listID,listData in ikv(spriteData["lists"]):
            name = listData[0]
            currentValue = listData[1]
            if spriteData["isStage"]:
                mode = "global"
                sprite = None
            else:
                mode = "local"
                sprite = spriteData["name"]
            newListData = {
                "name"        : name,
                "currentValue": currentValue,
                "mode"        : mode,
                "sprite"      : sprite,
            }
            newData.append(newListData)
    return newData

def generateBlockChildrenPs(data):
    blockParentPs = {k:v["parent"] for i,k,v in ikv(data)} # Get all block's parents
    blockChildrenPs = {k:[] for k in data.keys()} # Create an empty dict which records each block's children
    # Add each block to their parent's children list
    #print(blockParentPs)
    ancestorPs = []
    for i,childP,parentP in ikv(blockParentPs):
        #print(k,parentP)
        if parentP != None:
            blockChildrenPs[parentP].append(childP)
        opcodeData = opcodeDatabase[data[childP]["opcode"]]
        #if opcodeData["type"] == "instruction" and parentP == None:
        if parentP == None:
            ancestorPs.append(childP)
    return ancestorPs, blockChildrenPs

def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        pp(costumeData)
        newCostumeData = {
            "name"            : costumeData["name"],
            "bitmapResolution": None,
            "dataFormat"      : costumeData["dataFormat"],
            "fileStem"        : costumeData["assetId"],
            "rotationCenter"  : [costumeData["rotationCenterX"], costumeData["rotationCenterY"]],
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
        pp(soundData)
        newSoundData = {
            "name"       : soundData["name"],
            "dataFormat" : soundData["dataFormat"],
            "fileStem"   : soundData["assetId"],
            "rate"       : soundData["rate"],        # playback speed in Hz
            "sampleCount": soundData["sampleCount"], # = "rate" * duration in secs
        }
        newSoundDatas.append(newSoundData)
    return newSoundDatas

def optimizeProject(sourcePath, targetPath):
    dataSource = readJSONFile(sourcePath)
    newSpriteDatas = []
    pp(dataSource)
    for i, spriteData in enumerate(dataSource["targets"]):
        commentDatas = spriteData["comments"]
        floatingCommentDatas = [] # The comments that aren't connected to any blocks
        for commentData in commentDatas.values():
            if commentData["blockId"] == None: # No Block connection
                floatingCommentDatas.append(translateComment(data=commentData))
        ancestorPs, blockChildrenPs = generateBlockChildrenPs(data=spriteData["blocks"])
        newScriptDatas = []
        for ancestorP in ancestorPs:
            newScriptData = translateScript(
                data=spriteData["blocks"], 
                ancestorP=ancestorP, 
                blockChildrenPs=blockChildrenPs,
                commentDatas=commentDatas,
            )
            newScriptDatas.append(newScriptData)
        translatedCostumeDatas = translateCostumes(data=spriteData["costumes"])
        translatedSoundDatas   = translateSounds  (data=spriteData["sounds"])
        #print(ancestorPs)
        #pp(blockResults)
        newSpriteData = {
            "isStage"       : i == 0,
            "name"          : spriteData["name"],
            "scripts"       : newScriptDatas,
            "comments"      : floatingCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : translatedCostumeDatas,
            "sounds"        : translatedSoundDatas,
            "volume"        : spriteData["volume"],
            "layerOrder"    : spriteData["layerOrder"],
        }
        if spriteData["isStage"]:
            newSpriteData |= {
                "tempo"               : spriteData["tempo"],
                "videoTransparency"   : spriteData["videoTransparency"],
                "videoState"          : spriteData["videoState"],
                "textToSpeechLanguage": spriteData["textToSpeechLanguage"],
            }
        else:
            newSpriteData |= {
                "visible"      : spriteData["visible"],
                "position"     : [spriteData["x"], spriteData["y"]],
                "size"         : spriteData["size"],
                "direction"    : spriteData["direction"],
                "draggable"    : spriteData["draggable"],
                "rotationStyle": spriteData["rotationStyle"],
            }
        newSpriteDatas.append(newSpriteData)
    newData = {
        "sprites"      : newSpriteDatas,
        "variables"    : translateVariables(data=dataSource["targets"]),
        "lists"        : translateLists    (data=dataSource["targets"]),
        "monitors"     : dataSource["monitors"],
        "extensionData": dataSource["extensionData"],
        "extensions"   : dataSource["extensions"],
        "meta"         : dataSource["meta"],
    }
    pp(newData)
    writeJSONFile(targetPath, newData)

optimizeProject(
    sourcePath="test.json",#"source.json", 
    targetPath="optimized3.json",
)
