from pypenguin.helper_functions import pp
from pypenguin.database import opcodeDatabase

import copy

def completeProject(projectData):
    data = copy.deepcopy(projectData)
    for spriteData in data["sprites"]:
        for scriptData in spriteData["scripts"]:
            for blockData in scriptData["blocks"]:
                completeBlock(blockData)

def completeBlock(blockData):
    if "inputs" not in blockData:
        blockData["inputs"] = {}
    if "options" not in blockData:
        blockData["options"] = {}
    if "comment" not in blockData:
        blockData["comment"] = None

def completeInput(inputData, opcode):
    opcodeData = opcodeDatabase[opcode]
    if opcode == "call ...": # Inputs in the call block type are custom
        proccode, inputTypes = parseCustomOpcode(optionDatas["customOpcode"])
        inputTypes = {k: ("text" if v==str else "boolean") for i,k,v in ikv(inputTypes)}
    else:
        inputTypes = opcodeData["inputTypes"]
    
    inputType = inputTypes[inputID]
    match inputType: # type of the input
        case "broadcast"|"integer"|"positive integer"|"number"|"text":
            inputMode = "block-and-text"
        case "boolean"|"round":
            inputMode = "block-only"
        case "script":
            inputMode = "script"
    
    if "mode" not in inputValue:
        inputValue["mode"] = inputMode
    
    