import json, copy

from pypenguin.utility import numberToLiteral, BlockSelector, generateRandomToken, parseCustomOpcode, stringToToken, LocalStringToToken, Platform, getSelectors, editDataStructure, removeDuplicates
from pypenguin.deoptimize.options import translateOptions
from pypenguin.deoptimize.comments import translateComment
from pypenguin.database import *

def completeScripts(data):
    def completeBlock(data):
        newInputDatas = {}
        for inputID, inputData in data.get("inputs", {}).items():
            if opcode == "procedures_call":
                argument  = arguments[inputID]
                if   argument == str:
                    inputType = "text"
                    inputMode = "block-and-text"
                elif argument == bool:
                    inputType = "boolean"
                    inputMode = "block-only"
            else:
                inputType = getInputType(
                    opcode=opcode, 
                    inputID=inputID,
                )
                inputMode = getInputMode(
                    opcode=opcode, 
                    inputID=inputID,
                )
            inputData["mode"]   = inputMode
            inputData["_type_"] = inputType
        
            if   inputMode in ["block-and-text", "block-and-menu-text"]:
                required = ["block", "text"]
            elif inputMode == "block-only":
                required = ["block"]
            elif inputMode in ["block-and-option", "block-and-broadcast-option"]:
                required = ["option"]
            elif inputMode == "script":
                required = ["blocks"]
            
            for attribute in required:
                if attribute not in inputData:
                    match attribute:
                        case "block":
                            inputData["block"] = inputBlockDefault
                        case "text":
                            if inputType == "note":
                                inputData["text"] = noteInputTextDefault
                            else:
                                inputData["text"] = inputTextDefault
                        case "blocks":
                            inputData["blocks"] = inputBlocksDefault
                        case "option":
                            raise Exception()
            newInputDatas[inputID] = inputData
          
        newBlockData = {
            "opcode": data["opcode"],
            "inputs": newInputDatas,
            "options": newOptionDatas,
            "comment": data.get("comment", None),
        }
    
    def completeBlocks(data):
        newBlockDatas = []
        for blockData in data:
            newBlockDatas.append(completeBlock(blockData))
        
    newScriptDatas = []
    for scriptData in data:
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks": completeBlocks(scriptData["blocks"]),
        })

def prepareScripts(data):
    newScriptDatas = []
    for scriptData in data:
        newBlockDatas = []
        for i, blockData in enumerate(scriptData["blocks"]):
            newBlockDatas.append(prepareBlock(
                data=blockData,
                parentOpcode=None,
                position=scriptData["position"] if i == 0 else None
            ))
        newScriptDatas.append({
            "position": scriptData["position"],
            "blocks"  : newBlockDatas,
        })
    return newScriptDatas

def generateMenu(data, parentOpcode, inputID):
    opcode = getDeoptimizedOpcode(opcode=parentOpcode)
    menu = getMenu(
        opcode=opcode,
        inputID=inputID,
    )
    menuOpcode = getOptimizedOpcode(opcode=menu["menuOpcode"])
    newData = {
        "opcode" : menuOpcode,
        "inputs" : {},
        "options": {
            menu["inner"]: data,
        },
    }
    return newData
    """ eg. "_mouse_" ->
    {
        "opcode": "#TOUCHING OBJECT MENU",
        "inputs": {},
        "options": {"TOUCHINGOBJECTMENU": "_mouse_"},
        "_info_": ...,
    }"""

def prepareBlock(data, parentOpcode, position=None, isOption=False, inputID=None):
    isMenu = False
    if isinstance(data, str):
        if not isOption: raise Exception()
        # When the block is a menu value
        data = generateMenu(
            data=data,
            parentOpcode=parentOpcode,
            inputID=inputID,
        )
        isMenu = True
    
    
    if "inputs" not in data:
        data["inputs"] = inputDefault
    if "options" not in data:
        data["options"] = optionDefault
    opcode = getDeoptimizedOpcode(opcode=data["opcode"])
    if opcode == "procedures_call":
        proccode, arguments = parseCustomOpcode(customOpcode=data["options"]["customOpcode"][1])
    newInputDatas = {}
    for inputID, inputData in data["inputs"].items():
        if opcode == "procedures_call":
            argument  = arguments[inputID]
            if   argument == str:
                inputType = "text"
                inputMode = "block-and-text"
            elif argument == bool:
                inputType = "boolean"
                inputMode = "block-only"
        else:
            inputType = getInputType(
                opcode=opcode, 
                inputID=inputID,
            )
            inputMode = getInputMode(
                opcode=opcode, 
                inputID=inputID,
            )
        inputData["mode"]   = inputMode
        inputData["_type_"] = inputType
    
        if   inputMode in ["block-and-text", "block-and-menu-text"]:
            required = ["block", "text"]
        elif inputMode == "block-only":
            required = ["block"]
        elif inputMode in ["block-and-option", "block-and-broadcast-option"]:
            required = ["option"]
        elif inputMode == "script":
            required = ["blocks"]
        
        for attribute in required:
            if attribute not in inputData:
                match attribute:
                    case "block":
                        inputData["block"] = inputBlockDefault
                    case "text":
                        if inputType == "note":
                            inputData["text"] = noteInputTextDefault
                        else:
                            inputData["text"] = inputTextDefault
                    case "blocks":
                        inputData["blocks"] = inputBlocksDefault
                    case "option":
                        raise Exception()
        newInputDatas[inputID] = inputData
    
    inputDatas = newInputDatas
    newInputDatas = {}
    for inputID, inputData in inputDatas.items():
        if inputData["mode"] == "block-and-broadcast-option":
            inputData["text"] = inputData["option"]
            del inputData["option"]
        if inputData["mode"] == "block-and-menu-text":
            inputData["option"] = ["value", inputData["text"]]
            del inputData["text"]
        newInputData = copy.deepcopy(inputData)
        if inputData.get("block") != None:
            newInputData["block"]  = prepareBlock(
                data=inputData["block"],
                parentOpcode=data["opcode"],
            )
        if inputData.get("blocks") != None:
            newInputData["blocks"] = [prepareBlock(
                data=subBlockData,
                parentOpcode=data["opcode"],
            ) for subBlockData in inputData["blocks"]]
        if inputData.get("option") != None:
            newOptionData = deoptimizeOptionValue(
                optionValue=inputData["option"],
                optionType=inputData["_type_"],
            )
            newInputData["option"] = prepareBlock(
                data=newOptionData,
                parentOpcode=data["opcode"],
                isOption=True,
                inputID=inputID,
            )
        del newInputData["_type_"]    
        newInputDatas[inputID] = newInputData
        
    if isMenu:
        newOptionDatas = data["options"]
    else:
        newOptionDatas = {}
        for optionID, optionData in data["options"].items():
            optionType = getOptionType(
                opcode=opcode,
                optionID=optionID,
            )
            newOptionData = deoptimizeOptionValue(
                optionValue=optionData,
                optionType=optionType,
            )
            newOptionDatas[optionID] = newOptionData
    
    newData = data | {
        "inputs" : newInputDatas,
        "options": newOptionDatas,
        "_info_" : {
            "position": position,
            "topLevel": position != None,
        },
    }
    return newData

def flattenScripts(data):
    newBlockDatas = {}
    for i, scriptData in enumerate(data):
        # Generate IDs for the blocks
        newBlockDatas |= flattenBlocks(
            data=scriptData["blocks"],
            placementPath=[i]+["blocks"],
        )
    return newBlockDatas

def flattenBlocks(data, placementPath, parentID=None, firstID=None):
    range_ = range(len(data))
    blockIDs = [BlockSelector() for i in range_]
    if firstID != None:
        blockIDs[0] = firstID
    newBlockDatas = {}
    for i, blockData in enumerate(data):
        blockID = blockIDs[i]
        if i - 1 in range_: # When the block has a upwards neighbour
            parentID = blockIDs[i - 1]
        elif i == 0:
            parentID = parentID
        if i + 1 in range_: # When the block has a downwards neighbour
            nextID = blockIDs[i + 1]
        else:
            nextID = None
        
        newBlockDatas |= flattenBlock(
            data=blockData,
            blockID=blockID,
            parentID=parentID,
            nextID=nextID,
            placementPath=placementPath+[i],
        )
    return newBlockDatas

def flattenBlock(data, blockID, parentID, nextID, placementPath):
    # Transform inputs
    newBlockDatas = {}
    newInputDatas = {}
    for inputID, inputData in data["inputs"].items():
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
                subBlockID = BlockSelector()
                references.append(subBlockID)
                newBlockDatas |= flattenBlock(
                    data=inputData["block"],
                    placementPath=placementPath+["inputs"]+[inputID]+["block"],
                    blockID=subBlockID,
                    parentID=blockID,
                    nextID=None,
                )
        if inputData.get("blocks", []) != []:
            subBlockID = BlockSelector()
            references.append(subBlockID)
            newBlockDatas |= flattenBlocks(
                data=inputData["blocks"],
                placementPath=placementPath+["inputs"]+[inputID]+["blocks"],
                parentID=blockID,
                firstID=subBlockID,
            )
        if inputData.get("option") != None:
            subBlockID = BlockSelector()
            references.append(subBlockID)
            newBlockDatas |= flattenBlock(
                data=inputData["option"],
                placementPath=placementPath+["inputs"]+[inputID]+["option"],
                blockID=subBlockID,
                parentID=blockID,
                nextID=None,
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
        "comment": data.get("comment"),
        "_info_" : data["_info_"] | {
            "parent"  : parentID,
            "next"    : nextID,
        },
        "_placementPath_": placementPath, #eg. 1 indicates an origin from the 1st script 
    }
    newBlockDatas[blockID] = newBlockData
    return newBlockDatas

def restoreProcedureDefinitionBlock(data, blockID):
    customOpcode        = data["options"]["customOpcode"]
    proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
    argumentIDs         = []
    argumentNames       = []
    argumentDefaults    = []
    argumentBlockIDs    = []
    for argumentName, argumentType in arguments.items():
        argumentIDs     .append(generateRandomToken())
        argumentNames   .append(argumentName)
        # The argument reporter defaults
        argumentDefaults.append("" if argumentType==str else json.dumps(False))
        argumentBlockIDs.append(BlockSelector())
    
    match data["options"]["blockType"]:
        case "instruction"    : returns, optype, opcode = False, "statement", "procedures_definition"
        case "lastInstruction": returns, optype, opcode = None , "end"      , "procedures_definition"
        case "textReporter"   : returns, optype, opcode = True , "string"   , "procedures_definition_return" 
        case "numberReporter" : returns, optype, opcode = True , "number"   , "procedures_definition_return"
        case "booleanReporter": returns, optype, opcode = True , "boolean"  , "procedures_definition_return"
    
    definitionID = blockID
    prototypeID  = BlockSelector()
    position     = data["_info_"]["position"]
    definitionData = {
        "opcode": opcode,
        "next": data["_info_"]["next"],
        "parent": None,
        "inputs": {"custom_block": [1, prototypeID]},
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": position[0],
        "y": position[1],
        "_placementPath_": data["_placementPath_"],
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
            "warp"            : json.dumps(data["options"]["noScreenRefresh"]),
            "returns"         : json.dumps(returns),
            "edited"          : json.dumps(True),
            "optype"          : json.dumps(optype),
            "color"           : json.dumps(["#FF6680", "#eb3d5b", "#df2847"]),
        },
        "_placementPath_": data["_placementPath_"]+["CB_PROTOTYPE"],
    }
    newBlockDatas = {}
    newBlockDatas[definitionID] = definitionData
    newBlockDatas[prototypeID]  = prototypeData
    for j in range(len(argumentIDs)):
        argumentName = argumentNames[j]
        newBlockDatas[argumentBlockIDs[j]] = {
            "opcode": "argument_reporter_string_number" if argumentDefaults[j] == "" else "argument_reporter_boolean",
            "next": None,
            "parent": prototypeID,
            "inputs": {},
            "fields": {
                "VALUE": [argumentName, generateRandomToken()]
            },
            "shadow": True,
            "topLevel": False,
            "mutation": {
                "tagName": "mutation",
                "children": [],
                "color": "[\"#FF6680\",\"#eb3d5b\",\"#df2847\"]"
            },
            "_placementPath_": data["_placementPath_"]+["CB_PROTOTYPE_ARGS"]+[argumentName],
        }
    return newBlockDatas

def restoreBlocks(data, spriteName):
    newBlockDatas = {}
    newCommentDatas = {}
    for blockID, blockData in data.items():
        opcode = getDeoptimizedOpcode(opcode=blockData["opcode"])
        
        if opcode in ["special_variable_value", "special_list_value"]:
            newBlockData = restoreListBlock(
                data=blockData,
                spriteName=spriteName,
            )
        elif opcode in ["special_define"]:
            newBlockData = None
            newBlockDatas |= restoreProcedureDefinitionBlock(
                data=blockData,
                blockID=blockID,
            )
        else:
            blockType = getBlockType(opcode=opcode)
            if blockType == "menu":
                hasShadow = True
            elif opcode in ["polygon"]:
                hasShadow = True
            else:
                hasShadow = False
            
            newBlockData = {
                "opcode"  : opcode,
                "next"    : blockData["_info_"]["next"],
                "parent"  : blockData["_info_"]["parent"],
                "inputs"  : restoreInputs(
                    data=blockData["inputs"],
                    opcode=opcode,
                    spriteName=spriteName,
                    blockData=blockData,
                ),
                "fields"  : translateOptions(
                    data=blockData["options"],
                    opcode=opcode,
                    spriteName=spriteName,
                ),
                "shadow"  : hasShadow,
                "topLevel": blockData["_info_"]["topLevel"],
                "_placementPath_": blockData["_placementPath_"],
            }
            if blockData["_info_"]["position"] != None:
                position = blockData["_info_"]["position"]
                newBlockData |= {"x": position[0], "y": position[1]}
        
        if blockData.get("comment") != None:
            newCommentData = translateComment(
                data=blockData["comment"],
                id=blockID,
            )
            newCommentID = BlockSelector()
            newCommentDatas[newCommentID] = newCommentData
            newBlockData["comment"] = newCommentID
        
        if newBlockData != None:
            newBlockDatas[blockID] = newBlockData
    return newBlockDatas, newCommentDatas

def restoreInputs(data, opcode, spriteName, blockData):
    newInputDatas = {}
    if opcode == "procedures_call":
        proccode, arguments = parseCustomOpcode(customOpcode=blockData["options"]["customOpcode"])
    for inputID, inputData in data.items():
        if opcode == "procedures_call":
            argument = arguments[inputID]
            if   argument == str:
                inputType = "text"
                inputMode = "block-and-text"
            elif argument == bool:
                inputType = "boolean"
                inputMode = "block-only"
        else:
            inputType = getInputType(
                opcode=opcode,
                inputID=inputID
            )
            inputMode = getInputMode(
                opcode=opcode,
                inputID=inputID
            )
        
        subBlocks     = inputData["references"]
        if inputData["listBlock"] != None:
            subBlocks.insert(0, restoreListBlock(
                data=inputData["listBlock"],
                spriteName=spriteName,
            ))
        subBlockCount = len(subBlocks)
        match inputMode:
            case "block-and-text"|"block-and-broadcast-option":
                magicNumber = getInputMagicNumber(inputType=inputType)
                if inputMode == "block-and-broadcast-option":
                    text = inputData["text"][1]
                    token = stringToToken(text)
                    textData = [magicNumber, text, token]
                else:
                    textData = [magicNumber, inputData["text"]]
                if   subBlockCount == 0:
                    newInputData = [1, textData]
                elif subBlockCount == 1:
                    newInputData = [3, subBlocks[0], textData]
                textData = [magicNumber, inputData["text"]]
            case "block-only"|"script":
                if   subBlockCount == 0:
                    newInputData = None
                elif subBlockCount == 1:
                    newInputData = [2, subBlocks[0]]
            case "block-and-option"|"block-and-menu-text":
                if   subBlockCount == 1:
                    newInputData = [1, subBlocks[0]]
                elif subBlockCount == 2:
                    newInputData = [3, subBlocks[0],  subBlocks[1]]
        
        
        newInputID = getDeoptimizedInputID(
            opcode=opcode,
            inputID=inputID,
        )
        if newInputData != None:
            newInputDatas[newInputID] = newInputData
    return newInputDatas

def restoreListBlock(data, spriteName):
    if   data["opcode"] == getOptimizedOpcode(opcode="special_variable_value"):
        magicNumber = 12
        value = data["options"]["VARIABLE"]
    elif data["opcode"] == getOptimizedOpcode(opcode="special_list_value"    ):
        magicNumber = 13
        value = data["options"]["LIST"]
    
    token = LocalStringToToken(value, spriteName=spriteName)
    newData = [magicNumber, value, token]
    if data["_info_"]["topLevel"]:
        newData += data["_info_"]["position"]
    # No _placementPath_ needed. In cases, where list blocks are not contained within other blocks, they shouldn't impact performance too much.
    return newData

def unprepareBlocks(data):
    mutationDatas = {}
    for blockData in data.values():
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    newBlockDatas = {}
    for blockID, blockData in data.items():
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_call":
                customOpcode = blockData["fields"]["customOpcode"]
                del blockData["fields"]["customOpcode"]
                proccode, arguments = parseCustomOpcode(customOpcode=customOpcode)
                mutationData         = mutationDatas[proccode]
                modifiedMutationData = mutationData.copy()
                del modifiedMutationData["argumentnames"]
                del modifiedMutationData["argumentdefaults"]
                blockData["mutation"] = modifiedMutationData
        
                argumentIDs   = json.loads(mutationData["argumentids"])
                argumentNames = json.loads(mutationData["argumentnames"])
                blockData["inputs"] = {
                    argumentIDs[argumentNames.index(inputID)]: 
                    inputValue for inputID,inputValue in blockData["inputs"].items() 
                }

            elif blockData["opcode"] == "control_stop":
                match blockData["fields"]["STOP_OPTION"][0]:
                    case "all" | "this script"    : hasNext = False
                    case "other scripts in sprite": hasNext = True
                blockData["mutation"] = {
                    "tagName": "mutation",
                    "children": [],
                    "hasnext": json.dumps(hasNext)
                }
            
            elif blockData["opcode"] == "polygon":
                blockData["mutation"] = { # seems to alwys be constant
                    "tagName": "mutation",
                    "children": [],
                    "points": json.dumps(blockData["fields"]["VERTEX_COUNT"][0]), # TODO: research
                    "color": "#0FBD8C",
                    "midle": "[0,0]",
                    "scale": "50",
                    "expanded": "false"
                }
                del blockData["fields"]["VERTEX_COUNT"]
            newBlockDatas[blockID] = blockData
    return newBlockDatas

from pypenguin.utility import pp

# Replaces block selectors with literals eg. "t"
def makeJsonCompatible(data, commentDatas, targetPlatform):  
    selectors = removeDuplicates(getSelectors(data) + getSelectors(commentDatas))
    # Translation table from selector object to literal
    if   targetPlatform == Platform.PENGUINMOD:
        table = {selector: numberToLiteral(i+1)  for i, selector in enumerate(selectors)}
    elif targetPlatform == Platform.SCRATCH:
        table = {selector: generateRandomToken() for    selector in           selectors }
    def conversionFunc(obj):
        nonlocal table
        if isinstance(obj, BlockSelector):
            return table[obj]
        if isinstance(obj, LocalStringToToken):
            return obj.toToken()
    conditionFunc = lambda obj: isinstance(obj, (BlockSelector, LocalStringToToken))
    data         = editDataStructure(data        , conditionFunc=conditionFunc, conversionFunc=conversionFunc)
    commentDatas = editDataStructure(commentDatas, conditionFunc=conditionFunc, conversionFunc=conversionFunc)
    return data, commentDatas
