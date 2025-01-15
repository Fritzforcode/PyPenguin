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

def setVar(variable, valueBlock=None, valueText=None):
    block = Block("set [VARIABLE] to (VALUE)")
    block.addInput("VALUE", blockArg=valueBlock, text=valueText)
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

def operation(operation, leftBlock, rightBlock=None, rightText=None):
    block = Block("(OPERAND1) " + operation + " (OPERAND2)")
    block.addInput("OPERAND1", blockArg=leftBlock)
    block.addInput("OPERAND2", blockArg=rightBlock, text=rightText)
    return block

def defineCustomBlock(customOpcode, blockType, noScreenRefresh=True):
    block = Block("define custom block")
    block.addOption("noScreenRefresh", "value", noScreenRefresh)
    block.addOption("blockType"      , "value", blockType      )
    block.addOption("customOpcode"   , "value", customOpcode   )
    return block

def switchCases(switchBlock, cases):
    caseValues = list(cases.keys())
    caseBodies = list(cases.values())
    cases = []
    for caseValue, caseBody in zip(caseValues, caseBodies):
        caseBlock = Block("case (CONDITION) {BODY}")
        if isinstance(caseValue, str):
            caseBlock.addInput("CONDITION", text=caseValue)
        else:
            caseBlock.addInput("CONDITION", block=caseValue)
        caseBlock.addInput("BODY", caseBody)
        cases.append(caseBlock)
    
    block = Block("switch (CONDITION) {CASES}")
    block.addInput("CONDITION", blockArg=switchBlock)
    block.addInput("CASES", blockArg=cases)
    return block

project = {"sprites": [{"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["jgJSON"]}

from pprint import pprint
variables = ["xcv cached"]

compare = operation("!=", getArg("xcv"), getVar("xcv cached"))
then    = setVar("xcv cached", getArg("xcv"))
ifBlock = Block("if <CONDITION> then {THEN}")
ifBlock.addInput("CONDITION", compare).addInput("THEN", [then])
script  = Script([0,0])

cases = {
    "a": [Block("say (MESSAGE)").addInput("MESSAGE", text="Hello")],
    "b": [Block("say (MESSAGE)").addInput("MESSAGE", text="Moin")],
    "c": [Block("say (MESSAGE)").addInput("MESSAGE", text="Salve")],
}

switch = switchCases(getVar("xcv cached"), cases)

script.addBlock(ifBlock)
script.addBlock(switch)

pprint(script.toJSON(), indent=4, sort_dicts=False)
scripts = [script]

import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.utility import writeJSONFile
project["sprites"][0]["scripts"] = [script.toJSON() for script in scripts]
project["globalVariables"] = [{"name":variable, "currentValue":"", "isCloudVariable":False} for variable in variables]
validateProject(projectData=project)

writeJSONFile(
    filePath = "project/project.json",
    data     = project
)

writeJSONFile(
    filePath = "temp2.json",
    data     = project
)

deoptimizeAndCompressProject(
    optimizedProjectDir      = "project",
    projectFilePath          = "export.pmp",
    temporaryDir             = "temporary",
    #deoptimizedDebugFilePath = "temp_wrong.json",
)
