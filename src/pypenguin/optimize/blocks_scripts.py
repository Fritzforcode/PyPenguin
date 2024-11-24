from pypenguin.helper_functions import ikv, pp
from pypenguin.database import getOptimizedOpcode, getOptimizedInputID, getInputMode

def prepareBlocks(data):
    newData = {}
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, list): # For list blocks e.g. value of a variable
            newBlockData = prepareListBlock(data=blockData)
        else: # For normal blocks
            newBlockData = {
                "opcode"      : getOptimizedOpcode(opcode=blockData["opcode"]),
                "inputs"      : prepareInputs(
                    data=blockData["inputs"],
                    opcode=blockData["opcode"],
                ),
                "options"     : prepareOptions(data=blockData["fields"]),
                "_info_"      : {
                    "position": None,
                    "next"    : blockData["next"],
                    "topLevel": blockData["topLevel"],
                },
            }
            if "x" in blockData and "y" in blockData:
                newBlockData["_info_"]["position"] = [blockData["x"], blockData["y"]]
            #TODO: implement comments, custom blocks
            #if comment != None:
            #    newData["comment"] = comment
            #if mutation != None:
            #    newData["mutation"] = mutation
        newData[blockID] = newBlockData
    return newData

def nestScripts(data):
    for i, blockID, blockData in ikv(data):
        if blockData["_info_"]["topLevel"]:
            nestBlockRecursively(
                blockDatas=data,
                blockID=blockID,
            )
            raise Exception(".")

def nestBlockRecursively(blockDatas, blockID):
    blockData = blockDatas[blockID]
    pp(blockData)
    for i, inputID, inputData in ikv(blockData["inputs"]):
        subBlockDatas = []
        print(inputID, inputData)
        for reference in inputData["references"]: 
            subBlockDatas.append(nestBlockRecursively(
                blockDatas=blockDatas,
                blockID=reference,
            ))
        if inputData["listBlock"] != None:
            subBlockDatas.append(inputData["listBlock"])
        
        blockCount = len(subBlockDatas)
        match 
        

def prepareInputs(data, opcode):
    # Replace the old with the new input ids
    newData = {}
    for i, inputID, inputData in ikv(data):
        newInputID = getOptimizedInputID(
            opcode=opcode, 
            inputID=inputID,
        )
        newData[newInputID] = inputData
    data = newData
    
    # Optimize the input values
    newData = {}
    for i, inputID, inputData in ikv(data):
        #magicNumber = inputData[0]
        itemOneType = type(inputData[1])
        references = []
        listBlock  = None
        text       = None
        if   len(inputData) == 2:
            if   itemOneType == str: # e.g. "CONDITION": [2, "b"]
                # one block only, no text
                references.append(inputData[1])
            elif itemOneType == list: # e.g. "MESSAGE": [1, [10, "Bye!"]]
                # one block(currently empty) and text
                text = inputData[1][1]
        elif len(inputData) == 3:
            itemTwoType = type(inputData[2])
            if   itemOneType == str and itemTwoType == str: # e.g. "TOUCHINGOBJECTMENU": [3, "d", "e"]
                # two blocks(a menu, and a normal block) and no text
                references.append(inputData[1])
                references.append(inputData[2])
            elif itemOneType == str and itemTwoType == list: # e.g. 'OPERAND1': [3, 'e', [10, '']]
                # one block and text
                references.append(inputData[1])
                text = blockData[2][1]
            elif itemOneType == list: # e.g. 'VALUE': [3, [12, 'var', '=!vkqJLb6ODy(oqe-|ZN'], [10, '0']]
                # one list block and text
                listBlock = inputData[1]
                text = blockData[2][1]
        print(opcode)
        mode = getInputMode(
            opcode=opcode,
            inputID=inputID,
        )
        newInputData = {
            "mode"      : mode,
            "references": references,
            "listBlock" : listBlock,
            "text"      : text,
        }
        newData[inputID] = newInputData
    return newData    

def prepareOptions(data):
    return data

def prepareListBlock(data):
    # A variable or list block
    if data[0] == 12: # A magic value
        newData = {
            "opcode": "value of [VARIABLE]",
            "inputs": {},
            "options": {"VARIABLE": data[1]},
            "_info_"      : {
                "position": None,
                "next"    : None,
                "topLevel": False,
            },
        }
    elif data[0] == 13: # A magic value
        newData = {
            "opcode": "value of [LIST]",
            "inputs": {},
            "options": {"LIST": data[1]},
            "_info_"      : {
                "position": None,
                "next"    : None,
                "topLevel": False,
            },
        }
    raise Exception() # Correct the following code
    if len(data) > 3:
        newData["_info_"]["position"] = data[4:6]
        newData["_info_"]["topLevel"] = True
        
        
    return newData

def getCustomBlockMutations(data):
    mutationDatas = {}
    for i, blockID, blockData in ikv(data):
        if isinstance(blockData, dict):
            if blockData["opcode"] == "procedures_prototype":
                mutationData = blockData["mutation"]
                mutationDatas[mutationData["proccode"]] = mutationData
    return mutationDatas
