from helper_functions import ikv,  WhatIsGoingOnError, generateRandomToken,  readJSONFile, pp

opcodeDatabase = readJSONFile("assets/opcode_database.jsonc")


def translateOptions(optionDatas, opcode, spriteName, tokens):
    variableTokens = tokens["variables"]
    listTokens = tokens["lists"]
    broadcastTokens = tokens["broadcasts"]
    
    newData = {}
    opcodeData = opcodeDatabase[opcode]
    for i,optionID,optionData in ikv(optionDatas):
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
                else: raise WhatIsGoingOnError()
            elif optionData in tokens[spriteName]:
                nameKey = spriteName
            else:
                nameKey = None
            token = tokens[nameKey][optionData]
            newOptionData = [optionData, token, magicString]
        elif mode == "key":
            newOptionData = [optionData, generateRandomToken()]
        else: raise WhatIsGoingOnError()
        newData[optionID] = newOptionData
    return newData
