from pypenguin.helper_functions import ikv,  WhatIsGoingOnError, generateRandomToken,  readJSONFile, pp

from pypenguin.database import getOptionType, getBlockType, getDeoptimizedOptionID


def translateOptions(data, opcode, spriteName, tokens):
    blockType = getBlockType(opcode=opcode)
    if blockType == "menu":
        key = list(data.keys())[0]
        value = list(data.values())[0]
        return {key: [value, generateRandomToken()]}
    
    variableTokens  = tokens["variables"]
    listTokens      = tokens["lists"]
    broadcastTokens = tokens["broadcasts"]
    
    newData = {}
    for i,optionID,optionData in ikv(data):
        mode = getOptionType(
            opcode=opcode,
            optionID=optionID,
        )
        if mode in ["variable", "list", "broadcast"]:
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
                else: raise WhatIsGoingOnError()
            elif optionData in tokens[spriteName]:
                nameKey = spriteName
            else:
                nameKey = None
            token = tokens[nameKey][optionData]
            newOptionData = [optionData, token, magicString]
        elif mode in ["boolean", "round", "blockType", "opcode", "customBlockId"]:
            newOptionData = optionData
        else:
            newOptionData = [optionData, generateRandomToken()]
        
        newOptionID = getDeoptimizedOptionID(
            opcode=opcode,
            optionID=optionID,
        )
        newData[newOptionID] = newOptionData
    return newData
