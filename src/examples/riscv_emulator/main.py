import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, compressProject
from pypenguin.utility import writeJSONFile, pp, Platform
from helpers import *
import json

project = {"sprites": [{"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["jgJSON", "Bitwise"], "extensionURLs": {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}}

undefinedVariables = ["temp1", "temp2", "temp3", "temp4", "temp5", "instr_type", "instr", "arg0", "arg1", "arg2", "instructions", "current_instruction"]
definedVariables   = {
    "register_map": json.dumps({"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8, "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16, "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24, "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31, "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4, "t0": 5, "t1": 6, "t2": 7, "s0": 8, "s1": 9, "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27, "t3": 28, "t4": 29, "t5": 30, "t6": 31, "fp": 8}),
    "registers": json.dumps(32*[0]),
    "memory": json.dumps(16*[0]),
    "program_counter": json.dumps(0),
    "json_data": json.dumps({
        "description": "Memory load/store test",
        "instructions": [
            {"type": "arith", "instr": "addi", "arg0": "x5", "arg1": "x0", "arg2": 100},  # x5 = 100
            {"type": "store", "instr": "sw", "arg0": "x5", "arg1": "x0", "arg2": 0},  # Memory[0] = x5
            {"type": "load", "instr": "lw", "arg0": "x6", "arg1": "x0", "arg2": 0},  # x6 = Memory[0]
        ],
        "expected": {"x6": 100},  # x6 should be 100
    })
}

reset = Script([-1500, 0]).addBlocks([
    defineCustomBlock(customOpcode="reset", blockType="instruction"),
    setVar("registers", json.dumps([0]*32)),
    setVar("memory", json.dumps([0]*16)),
    setVar("program_counter", "0"),
])

regOrImm = Script([-1500, 500]).addBlocks([
    defineCustomBlock(customOpcode="reg or imm (value)", blockType="numberReporter"),
    ifThenElse(
        condition=Block("(STRING) is number?").addSmartInput("STRING", getArg("value")),
        then=[returnValue(getArg("value"))],
        otherwise=[returnValue(
            callCustomBlock("get register (register)")
            .addSmartInput("register", getArg("value"))
        )],
    ),
])

setMemory = Script([1000, 0]).addBlocks([
    defineCustomBlock(customOpcode="set memory (address) (size) to (value)", blockType="instruction"),
    *[ifThen(
        condition=operation(">=", left=getArg("size"), right=json.dumps(i+1)),
        then=[setVar("memory", setArrayIndexTo(
            array=getVar("memory"),
            index=operation("+", left=getArg("address"), right=json.dumps(i)),
            value=operation("and", left=bitwise(">>", num=getArg("value"), bits=json.dumps(8*i)), right="255"),
        ))],
    ) for i in range(4)],
])

getMemory = Script([2000, 0]).addBlocks([
    defineCustomBlock(customOpcode="get memory (address) (size) <signed>", blockType="numberReporter"),
    setVar("temp1", "0"),
    *[ifThen(
        condition=operation(">=", left=getArg("size"), right=json.dumps(i+1)),
        then=[changeVar("temp1", bitwise("<<", num=getArrayIndex(
            array=getVar("memory"),
            index=operation("+", left=getArg("address"), right=json.dumps(i)),
        ), bits=json.dumps(8*i)))],
    ) for i in range(4)],
    setVar("temp2", operation("*", left=getArg("size"), right="8")),
    ifThen(
        condition=boolOperation("and",
            left=getArg("signed", isBoolean=True),
            right=operation(">", left=getVar("temp1"), right=operation(
                "-", right="1", left=operation("^", left="2", right=operation(
                    "-", left=getVar("temp2"), right="1",
                ))
            ))
        ),
        then=[changeVar("temp1", operation("-", left="", right=operation("^", left="2", right=getVar("temp2"))))],
    ),
    returnValue(value=getVar("temp1"))
])

setRegister = Script([1000, 1200]).addBlocks([
    defineCustomBlock(customOpcode="set register (register) to (value)", blockType="instruction"),
    setVar("temp1", getJSONKey(json=getVar("register_map"), key=getArg("register"))),
    ifThen(
        condition=operation("!=", left=getVar("temp1"), right="0"),
        then=[setVar("registers", setArrayIndexTo(
            array=getVar("registers"),
            index=getVar("temp1"),
            value=operation("mod", left=getArg("value"), right=operation("^", "2", "32")),
        ))],
    )
])

getRegister = Script([2000, 1200]).addBlocks([
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
            ifThen(condition=operation("!=", left=getVar("instr"), right="lui"), then=[
                setVar("temp2", operation("+",
                    left=callCustomBlock("get register (register)").addSmartInput("register", getVar("arg1")),
                    right=callCustomBlock("reg or imm (value)").addSmartInput("value", getVar("arg2")),
                ))
            ]),
            switchCases(switch=getVar("instr"), cases={
                "lui": [setVar("temp3", bitwise("<<", num=getVar("arg1"), bits="12"))],
                "lw": [
                    setVar("temp3", callCustomBlock(customOpcode="get memory (address) (size) <signed>")
                    .addSmartInput("address", getVar("temp2"))
                    .addSmartInput("size", "4")
                    .addSmartInput("signed", Block("true")))
                ],
            }),
        ],
        "store": [
            switchCases(switch=getVar("instr"), cases={
                "sw": [
                    setVar("temp2", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg1"))),
                    ifThenElse(
                        condition=Block("(STRING) is number?").addSmartInput("STRING", getVar("arg2")),
                        then=[changeVar("temp2", getVar("arg2"))],
                        otherwise=[changeVar("temp2", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg2")))],
                    ),
                    callCustomBlock(customOpcode="set memory (address) (size) to (value)")
                    .addSmartInput("address", getVar("temp2"))
                    .addSmartInput("size", "__TEMP__")
                    .addSmartInput("value", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg0")))
                ],
            }),
        ],
        "arith": [
            setVar("temp2", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg1"))),
            ifThenElse(
                condition=Block("(STRING) is number?").addSmartInput("STRING", getVar("arg2")),
                then=[setVar("temp3", getVar("arg2"))],
                otherwise=[setVar("temp3", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg2")))],
            ),
            ifThen(condition=operation("=", left=getVar("instr"), right="addi"), then=[setVar("instr", "add")]),
            switchCases(switch=getVar("instr"), cases={
                "add": [setVar("temp4", operation("+"  , left=getVar("temp2"), right=getVar("temp3")))],
                "sub": [setVar("temp4", operation("-"  , left=getVar("temp2"), right=getVar("temp3")))],
                "and": [setVar("temp4", operation("and", left=getVar("temp2"), right=getVar("temp3")))],
                "or" : [setVar("temp4", operation("or" , left=getVar("temp2"), right=getVar("temp3")))],
                "xor": [setVar("temp4", operation("xor", left=getVar("temp2"), right=getVar("temp3")))],
            }),
            callCustomBlock("set register (register) to (value)")
            .addSmartInput("register", getVar("arg0")).addSmartInput("value", getVar("temp4")),
        ],
        "branch": [
            setVar("temp2", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg0"))),
            setVar("temp3", callCustomBlock(customOpcode="get register (register)").addSmartInput("register", getVar("arg1"))),
            setVar("temp4", operation("*", left=getVar("arg2"), right="2")),
            switchCases(switch=getVar("instr"), cases={
                "beq": [setVar("temp5", operation("=" , left=getVar("temp2"), right=getVar("temp3")))],
                "bne": [setVar("temp5", operation("!=", left=getVar("temp2"), right=getVar("temp3")))],
                "blt": [setVar("temp5", operation("<" , left=getVar("temp2"), right=getVar("temp3")))],
                "ble": [setVar("temp5", operation("<=", left=getVar("temp2"), right=getVar("temp3")))],
                "bgt": [setVar("temp5", operation(">" , left=getVar("temp2"), right=getVar("temp3")))],
                "bge": [setVar("temp5", operation(">=", left=getVar("temp2"), right=getVar("temp3")))],
            }),
            ifThen(condition=Block("(VALUE) as a boolean").addSmartInput("VALUE", getVar("temp5")), then=[
                changeVar("program_counter", operation("+", left="4", right=getVar("temp4"))),
                returnValue(value=""),
            ]),
        ],
    }),
    changeVar("program_counter", value="4"),
])

runProgram = Script([-1000, 0]).addBlocks([
    defineCustomBlock(customOpcode="run program (json_data)", blockType="instruction"),
    setVar("instructions", getJSONKey(json=getArg("json_data"), key="instructions")),
    whileBlock(condition=operation("<", 
        left=operation("/", left=getVar("program_counter"), right="4"),
        right=getArrayLength(array=getVar("instructions")),
    ), body=[
        setVar("current_instruction", 
            value=getArrayIndex(array=getVar("instructions"), 
            index=operation("/", left=getVar("program_counter"), right="4"))
        ),
        callCustomBlock(customOpcode="execute instruction (instruction)").addSmartInput("instruction", getVar("current_instruction"))
    ]),
])

pp(runProgram.toJSON())
scripts = [setMemory, getMemory, setRegister, getRegister, executeInstruction, runProgram, reset, regOrImm]

project["sprites"][0]["scripts"] = [script.toJSON() for script in scripts]
project["globalVariables"] = [{"name":variable, "currentValue":"", "isCloudVariable":False} for variable in undefinedVariables] + [{"name":variable, "currentValue":value, "isCloudVariable":False} for variable, value in definedVariables.items()]
#pp(project["sprites"][0]["scripts"][4]["blocks"][6]["inputs"]["CASES"]["blocks"][0]["inputs"]["BODY"]["blocks"][1]["inputs"]["CASES"]["blocks"][1]["inputs"]["BODY"]["blocks"][0]["inputs"]["VALUE"]["block"])
validateProject(projectData=project)

writeJSONFile(
    filePath = "project/project.json",
    data     = project
)

writeJSONFile(
    filePath = "temp2.json",
    data     = project
)
writeJSONFile("precompiled.json", [])
compressProject(
    optimizedProjectDir      = "project",
    projectFilePath          = "export.pmp",
    deoptimizedDebugFilePath = "temp_wrong.json",
    targetPlatform           = Platform.PENGUINMOD,
)
compressProject(
    optimizedProjectDir      = "project",
    projectFilePath          = "export.pmp",
    deoptimizedDebugFilePath = "temp_wrong.json",
    targetPlatform           = Platform.PENGUINMOD,
)
