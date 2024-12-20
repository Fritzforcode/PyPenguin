from pypenguin.helper_functions import ikv, removeDuplicates, stringToToken

from pypenguin.database import opcodeDatabase, inputDefault, inputTextDefault, optionDefault, deoptimizeOptionValue


def findBlockBroadcastMessages(data):
    for i,opcode,opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == data["opcode"]:
            break
    if not opcodeData["newOpcode"] == data["opcode"]: raise Exception(data["opcode"])

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

def generateBroadcasts(data):
    broadcastMessages = []
    for spriteData in data:
        for scriptData in spriteData["scripts"]:
            for blockData in scriptData["blocks"]:
                broadcastMessages += findBlockBroadcastMessages(data=blockData)
    broadcastMessages = removeDuplicates(broadcastMessages) # Remove duplicates
    newDatas = {}
    for broadcastMessage in broadcastMessages:
        broadcastMessage = deoptimizeOptionValue(
            optionValue=broadcastMessage,
            optionType="broadcast",
        )
        newDatas[broadcastMessage] = stringToToken(broadcastMessage)
    # Because all broadcast messages are for all sprites (None=Stage)
    return newDatas
