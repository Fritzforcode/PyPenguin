from exec_instr import executeInstr
from utility import *
from helpers import varReporterBlock
import json

instructions = [
    {"type": "move"      , "instr": "mov" , "arg0": "r0", "arg1": 10},  # r0 = 10
    {"type": "alu"       , "instr": "addi", "arg0": "r1", "arg1": "r0", "arg2": 5},  # r1 = r0 + 5
    {"type": "alu"       , "instr": "sub" , "arg0": "r2", "arg1": "r1", "arg2": 3},  # r2 = r1 - 3
    {"type": "alu"       , "instr": "mul" , "arg0": "r3", "arg1": "r2", "arg2": 2},  # r3 = r2 * 2
    {"type": "memory"    , "instr": "str" , "arg0": "r3", "arg1": "r0", "arg2": 4},  # Store r3 at r0 + 4
    {"type": "comparison", "instr": "cmp" , "arg0": "r3", "arg1": 14},  # Compare r3 with 14
    {"type": "branch"    , "instr": "bge" , "arg0": 9},  # Branch if r3 >= 14
    {"type": "move"      , "instr": "mov" , "arg0": "r4", "arg1": 1},  # r4 = 1 (won't execute if branch is taken)
    {"type": "branch"    , "instr": "b"   , "arg0": 10},  # Unconditional branch
    {"type": "move"      , "instr": "mov" , "arg0": "r4", "arg1": 0},  # r4 = 0
]

runProgram = {"position": [-1000, 0], "blocks": [
    {
        "opcode": "define custom block",
        "options": {"noScreenRefresh": ["value", True], "blockType": ["value", "instruction"], "customOpcode": ["value", "run program"]},
    },
    {
        "opcode": "while <CONDITION> {BODY}",
        "inputs": {
            "CONDITION": {"block": {
                "opcode": "(OPERAND1) < (OPERAND2)",
                "inputs": {
                    "OPERAND1": {"block": varReporterBlock("program counter")},
                    "OPERAND2": {"block": {
                        "opcode": "length of [LIST]",
                        "options": {"LIST": ["list", "instructions"]},
                    }},
                },
            }},
            "BODY": {"blocks": [
                {
                    "opcode": "set [VARIABLE] to (VALUE)",
                    "inputs": {
                        "VALUE": {"block": {
                            "opcode": "item (INDEX) of [LIST]",
                            "inputs": {
                                "INDEX": {"block": {
                                    "opcode": "(OPERAND1) + (OPERAND2)",
                                    "inputs": {
                                        "OPERAND1": {"block": varReporterBlock("program counter")},
                                        "OPERAND2": {"text": "1"},
                                    },
                                }},
                            },
                            "options": {"LIST": ["list", "instructions"]},
                        }},
                    },
                    "options": {"VARIABLE": ["variable", "current instruction"]},
                },
                {
                    "opcode": "call custom block",
                    "inputs": {
                        "instr": {"block": varReporterBlock("current instruction")},
                    },
                    "options": {"customOpcode": ["value", "execute instr (instr)"]},
                },
            ]},
        },
    },
]}

projectData = {
    "sprites": [
        {
            "name": "Stage",
            "isStage": True,
            "scripts": [
                setRegister,
                getRegister,
                setMemory,
                getMemory,
                getKeyElseDefault,
                executeInstr,
                runProgram,
            ],
            "comments": [],
            "currentCostume": 0,
            "costumes": [],
            "sounds": [],
            "volume": 100,
        },
    ],
    "globalVariables": [
        {
            "name": "program counter",
            "currentValue": "0",
            "isCloudVariable": False,
        },
        {
            "name": "register map",
            "currentValue": json.dumps({"r0": 0, "zero": 0, "r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6, "r7": 7, "r8": 8, "r9": 9, "sb": 9, "r10": 10, "sl": 10, "r11": 11, "fp": 11, "r12": 12, "ip": 12, "r13": 13, "sp": 13, "r14": 14, "lr": 14, "r15": 15, "pc": 15}),
            "isCloudVariable": False,
        },
        {
            "name": "memory",
            "currentValue": "{}",
            "isCloudVariable": False,
        },
        {
            "name": "flags",
            "currentValue": json.dumps({"zero": False, "negative": False}),
            "isCloudVariable": False,
        },
        *[{"name": name, "currentValue": "", "isCloudVariable": False} for name in ["instr", "instr type", "arg0", "arg1", "arg2", "value1", "value2", "result", "address", "do branch", "target pc", "current instruction"]],
    ],
    "globalLists": [
        {
            "name": "instructions",
            "currentValue": [json.dumps(instr) for instr in instructions],
        },
        {
            "name": "registers",
            "currentValue": 16*[0],
        },
    ],
    "monitors": [],
    "tempo": 60,
    "videoTransparency": 0,
    "videoState": "off",
    "textToSpeechLanguage": None,
    "extensionData": {},
    "extensions": ["jgJSON", "Bitwise"],
    "extensionURLs": {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"},
} # I was here

import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pypenguin import validateProject, deoptimizeAndCompressProject
from pypenguin.utility import writeJSONFile

validateProject(projectData=projectData)

writeJSONFile(
    filePath = "project/project.json",
    data     = projectData
)

writeJSONFile(
    filePath = "temp2.json",
    data     = projectData
)

deoptimizeAndCompressProject(
    optimizedProjectDir      = "project",
    projectFilePath          = "export.pmp",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp_wrong.json",
)
