from pypenguin.helper_functions import ikv,  WhatIsGoingOnError, generateRandomToken,  readJSONFile, pp

from pypenguin.database import opcodeDatabase


def translateOptions(optionDatas, opcode, spriteName, tokens):
    variableTokens = tokens["variables"]
    listTokens = tokens["lists"]
    broadcastTokens = tokens["broadcasts"]
    
    newData = {}
    opcodeData = opcodeDatabase[opcode]
    for i,optionID,optionData in ikv(optionDatas):
        print(optionID, optionData)
        mode = opcodeData["optionTypes"][optionID]
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
        elif mode == "key" or mode == "string":
            newOptionData = [optionData, generateRandomToken()]
        elif mode in ["boolean", "blockType", "opcode", "customBlockId"]:
            newOptionData = optionData
        else: raise WhatIsGoingOnError(mode)
        newData[optionID] = newOptionData
        print("-->", newOptionData)
    return newData
