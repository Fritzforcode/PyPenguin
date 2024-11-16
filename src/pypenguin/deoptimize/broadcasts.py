from pypenguin.helper_functions import ikv, WhatIsGoingOnError, generateRandomToken, readJSONFile, removeStringDuplicates, pp

from pypenguin.database import opcodeDatabase, inputDefault, inputTextDefault, optionDefault


def findBlockBroadcastMessages(data):
    for i,opcode,opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == data["opcode"]:
            break
    if not opcodeData["newOpcode"] == data["opcode"]: raise WhatIsGoingOnError(data["opcode"])
    
    broadcastMessages = []
    if "inputs" not in data:
        data["inputs"] = inputDefault
    for i,inputID,inputData in  ikv(data["inputs"]):
        if opcode != "procedures_call":
            if opcodeData["inputTypes"][inputID] == "broadcast":
                if "text" not in inputData:
                    inputData["text"] = inputTextDefault
                if inputData["text"] not in broadcastMessages:
                    broadcastMessages.append(inputData["text"])
            
        if "block" in inputData:
            if inputData["block"] != None:
                broadcastMessages += findBlockBroadcastMessages(data=inputData["block"])
    if "options" not in data:
        data["options"] = optionDefault
    for i,optionID,optionData in  ikv(data["options"]):
        if opcodeData["optionTypes"][optionID] == "broadcast":
            if optionData not in broadcastMessages:
                broadcastMessages.append(optionData)
    return broadcastMessages
    
def generateBroadcastTokens(data, spriteNames):
    broadcastMessages = []
    for spriteData in data:
        for scriptData in spriteData["scripts"]:
            for blockData in scriptData["blocks"]:
                broadcastMessages += findBlockBroadcastMessages(data=blockData)
    broadcastMessages = removeStringDuplicates(broadcastMessages) # Remove duplicates
    tokens = {}
    for broadcastMessage in broadcastMessages:
        tokens[broadcastMessage] = generateRandomToken()
    # Because all broadcast messages are for all sprites (None=Stage)
    newTokens = {spriteName:{} for spriteName in spriteNames}
    newTokens[None] = tokens 
    return newTokens
