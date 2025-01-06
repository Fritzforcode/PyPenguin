import copy

class BlockCls:
    def __init__(self, opcode):
        self.opcode = opcode
        self.inputs = {}
        self.options = {}
        self.comment = None
    def addInput(self, id, blockArg=None, text=None, option=None):
        data = {}
        if blockArg != None :
            if isinstance(blockArg, list): data["blocks"] = blockArg
            else                         : data["block" ] = blockArg
        if text != None  : data["text"  ] = text
        if option != None: data["option"] = option
        self.inputs[id] = data
        return self
    def addSmartInput(self, id, data):
        if isinstance(data, str):
            return self.addInput(id, text=data)
        else:
            return self.addInput(id, blockArg=data)
    def addOption(self, id, *args):
        if len(args) == 2:
            prefix = args[0]
            value = args[1]
        else:
            prefix = "value"
            value = args[0]
        self.options[id] = [prefix, value]
        return self
    def setComment(self, comment):
        self.comment = comment
        return self
    def toJSON(self):
        inputs = {}
        inputs_copy = copy.deepcopy(self.inputs)
        for id, value in zip(inputs_copy.keys(), inputs_copy.values()):
            inputs[id] = value
            if value.get("block") != None:
                inputs[id]["block"] = value["block"].toJSON()
            if value.get("blocks") != None:
                inputs[id]["blocks"] = [block.toJSON() for block in value["blocks"]]
        data = {"opcode": self.opcode}
        if       inputs != {}  : data["inputs" ] = inputs 
        if self.options != {}  : data["options"] = self.options
        if self.comment != None: data["comment"] = self.comment
        return data

def Block(opcode):
    block = BlockCls(opcode)
    return block

class ScriptCls:
    def __init__(self, position):
        self.position = position
        self.blocks   = []
    def addBlock(self, block):
        self.blocks.append(block)
        return self
    def addBlocks(self, blocks):
        self.blocks += blocks
        return self
    def toJSON(self):
        return {"position": self.position, "blocks": [block.toJSON() for block in self.blocks]}

def Script(position):
    script = ScriptCls(position)
    return script

def setVar(variable, value):
    block = Block("set [VARIABLE] to (VALUE)")
    block.addSmartInput("VALUE", value)
    block.addOption("VARIABLE", "variable", variable)
    return block    

def getVar(variable):
    block = Block("value of [VARIABLE]")
    block.addOption("VARIABLE", "variable", variable)
    return block

def getArg(arg, isBoolean=False):
    block = Block("value of boolean [ARGUMENT]" if isBoolean else "value of text [ARGUMENT]")
    block.addOption("ARGUMENT", "value", arg)
    return block

def operation(operation, left, right):
    block = Block("(OPERAND1) " + operation + " (OPERAND2)")
    block.addSmartInput("OPERAND1", left )
    block.addSmartInput("OPERAND2", right)
    return block

def bitwise(operation, num, bits):
    block = Block("(NUM) " + operation + " (BITS)")
    block.addSmartInput("NUM" , num )
    block.addSmartInput("BITS", bits)
    return block

def defineCustomBlock(customOpcode, blockType, noScreenRefresh=True):
    block = Block("define custom block")
    block.addOption("noScreenRefresh", "value", noScreenRefresh)
    block.addOption("blockType"      , "value", blockType      )
    block.addOption("customOpcode"   , "value", customOpcode   )
    return block

def callCustomBlock(customOpcode):
    block = Block("call custom block")
    block.addOption("customOpcode", customOpcode)
    return block

def returnValue(value):
    block = Block("return (VALUE)")
    block.addSmartInput("VALUE", value)
    return block

def switchCases(switch, cases):
    caseValues = list(cases.keys())
    caseBodies = list(cases.values())
    cases = []
    for caseValue, caseBody in zip(caseValues, caseBodies):
        caseBlock = Block("case (CONDITION) {BODY}")
        caseBlock.addSmartInput("CONDITION", caseValue)
        caseBlock.addSmartInput("BODY", caseBody)
        cases.append(caseBlock)
    
    block = Block("switch (CONDITION) {CASES}")
    block.addSmartInput("CONDITION", switch)
    block.addSmartInput("CASES", cases)
    return block

def setArrayIndexTo(array, index, value):
    block = Block("in array (ARRAY) set (INDEX) to (VALUE)")
    block.addSmartInput("ARRAY", array)
    block.addSmartInput("INDEX", index)
    block.addSmartInput("VALUE", value)
    return block

def getArrayIndex(array, index):
    block = Block("in array (ARRAY) get (INDEX)")
    block.addSmartInput("ARRAY", array)
    block.addSmartInput("INDEX", index)
    return block

def getJSONKey(json, key):
    block = Block("get (KEY) from (JSON)")
    block.addSmartInput("KEY" , key )
    block.addSmartInput("JSON", json)
    return block

def setJSONKeyTo(json, key, value):
    block = Block("set (KEY) to (VALUE) in (JSON)")
    block.addSmartInput("KEY"  , key  )
    block.addSmartInput("VALUE", value)
    block.addSmartInput("JSON" , json )
    return block

def ifThen(condition, then):
    block = Block("if <CONDITION> then {THEN}")
    block.addSmartInput("CONDITION", condition)
    block.addSmartInput("THEN"     , then     )
    return block
