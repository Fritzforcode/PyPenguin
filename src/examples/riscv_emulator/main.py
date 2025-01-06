import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.helper_functions import writeJSONFile, pp, Platform
from helpers import *
import json

project = {"sprites": [{"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["jgJSON", "Bitwise"], "extensionURLs": {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}}

undefinedVariables = ["temp1", "instr_type", "instr", "arg0", "arg1", "arg2"]
definedVariables   = {
    "register_map": json.dumps({"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8, "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16, "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24, "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31, "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4, "t0": 5, "t1": 6, "t2": 7, "s0": 8, "s1": 9, "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27, "t3": 28, "t4": 29, "t5": 30, "t6": 31, "fp": 8}),
    "registers": json.dumps(32*[0]),
    "memory": json.dumps(16*[0]),
}

setMemory = Script([1000, 0]).addBlocks([
    defineCustomBlock(customOpcode="set memory (address) to (value)", blockType="instruction"),
    setVar("memory", setArrayIndexTo(
        array=getVar("memory"),
        index=operation("+", left=getArg("address"), right="0"),
        value=operation("and", left=bitwise(">>", num=getArg("value"), bits="0"), right="255"),
    )),
    setVar("memory", setArrayIndexTo(
        array=getVar("memory"),
        index=operation("+", left=getArg("address"), right="1"),
        value=operation("and", left=bitwise(">>", num=getArg("value"), bits="8"), right="255"),
    )),
    setVar("memory", setArrayIndexTo(
        array=getVar("memory"),
        index=operation("+", left=getArg("address"), right="2"),
        value=operation("and", left=bitwise(">>", num=getArg("value"), bits="16"), right="255"),
    )),
    setVar("memory", setArrayIndexTo(
        array=getVar("memory"),
        index=operation("+", left=getArg("address"), right="3"),
        value=operation("and", left=bitwise(">>", num=getArg("value"), bits="24"), right="255"),
    )),
])

getMemory = Script([2000, 0]).addBlocks([
    defineCustomBlock(customOpcode="get memory (address)", blockType="numberReporter"),
    setVar("temp1", getArrayIndex(
        array=getVar("memory"),
        index=operation("+", left=getArg("address"), right="0"),
    )),
    setVar("temp1", operation(
        "+", left=getVar("temp1"),
        right=bitwise("<<", num=getArrayIndex(
            array=getVar("memory"),
            index=operation("+", left=getArg("address"), right="1"),
        ), bits="8"),
    )),
    setVar("temp1", operation(
        "+", left=getVar("temp1"),
        right=bitwise("<<", num=getArrayIndex(
            array=getVar("memory"),
            index=operation("+", left=getArg("address"), right="2"),
        ), bits="816"),
    )),
    setVar("temp1", operation(
        "+", left=getVar("temp1"),
        right=bitwise("<<", num=getArrayIndex(
            array=getVar("memory"),
            index=operation("+", left=getArg("address"), right="3"),
        ), bits="24"),
    )),
    returnValue(value=getVar("temp1"))
])

setRegister = Script([1000, 500]).addBlocks([
    defineCustomBlock(customOpcode="set register (register) to (value)", blockType="instruction"),
    setVar("temp1", getJSONKey(json=getVar("register_map"), key=getArg("register"))),
    ifThen(
        condition=operation("!=", left=getVar("temp1"), right="0"),
        then=[setVar("registers", setArrayIndexTo(
            array=getVar("registers"),
            index=getVar("temp1"),
            value=getArg("value"),
        ))],
    )
])

getRegister = Script([2000, 500]).addBlocks([
    defineCustomBlock(customOpcode="get register (register)", blockType="numberReporter"),
    returnValue(value=getArrayIndex(
        array=getVar("registers"),
        index=getJSONKey(json=getVar("register_map"), key=getArg("register"))
    ))
])

executeInstruction = Script([0, 0]).addBlocks([
    defineCustomBlock(customOpcode="execute instruction (instruction)", blockType="instruction"),
    setVar("instr_type", getJSONKey(json=getArg("instruction"), key="type")),
    setVar("instr", getJSONKey(json=getArg("instruction"), key="instr")),
    setVar("arg0", getJSONKey(json=getArg("instruction"), key="arg0")),
    setVar("arg1", getJSONKey(json=getArg("instruction"), key="arg1")),
    setVar("arg2", getJSONKey(json=getArg("instruction"), key="arg2")),
    switchCases(switch=getVar("instr_type"), cases={
        "load": [
            ifThen(condition=operation("=", getVar("instr"), "lui"), then=[
                callCustomBlock("set register (register) to (value)")
                .addSmartInput("register", getVar("arg0"))
                .addSmartInput("value", bitwise("<<", num=getVar("arg1"), bits="12"))
            ])
        ]
    })
])

pp(executeInstruction.toJSON())
scripts = [setMemory, getMemory, setRegister, getRegister, executeInstruction]

project["sprites"][0]["scripts"] = [script.toJSON() for script in scripts]
project["globalVariables"] = [{"name":variable, "currentValue":"", "isCloudVariable":False} for variable in undefinedVariables] + [{"name":variable, "currentValue":value, "isCloudVariable":False} for variable, value in definedVariables.items()]
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
    deoptimizedDebugFilePath = "temp_wrong.json",
    targetPlatform           = Platform.PENGUINMOD,
)
