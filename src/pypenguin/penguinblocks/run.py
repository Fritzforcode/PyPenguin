import subprocess
from pypenguin.utility import readJSONFile, writeJSONFile, pp
from pypenguin.database import getArgumentOrder, getOptimizedOpcode


# Define the code string and output file path
code = """
  move (length of [abcx]) steps
  if <[hi]=[bye]> then
    say [hi]
  else
    broadcast (abc v)
"""
jsPath     = "src/pypenguin/penguinblocks/main.js"
outputPath = "src/pypenguin/penguinblocks/in.json"

# Run the JavaScript file with arguments using Node.js
result = subprocess.run(
    ["node", jsPath, code, outputPath],
    capture_output=True,
    text=True,
)
if result.returncode == 0:
    if result.stdout != "": # When it isn't empty
        print("JavaScript output:", result.stdout)
else:
    print("Error:", result.stderr)

scripts = readJSONFile(outputPath)["scripts"]
#pp(scripts)

def createLiteral(literal):
    newLiteral = {
        "shape": literal["shape"],
        "text" : literal["value"] if literal["shape"] != "boolean" else None,
    }
    return newLiteral
    

def convertBlock(block):
    def isStandardOpcode(opcode) -> bool:
        return bool(opcode) and all(char.isupper() or char == '_' or char.isdigit() for char in opcode)
    arguments = []
    spec = "" # used for unrecognized blocks eg. "shout _" for "shout (Hi)"
    for child in block["children"]:
        if   "info" in child: # An input block
            arguments.append({"block": convertBlock(child)})
            spec += " [ARG]"
        elif "blocks" in child: # A blocks substack input
            arguments.append({"blocks": convertBlocks(child["blocks"])})
            spec += " [SUBSTACK]"
        elif "shape" in child: # An input or option literal
            arguments.append(createLiteral(child))
            spec += " [ARG]"
        elif "cls" in child: # block piece
            spec += " " + child["value"]
    spec = spec.strip()

    # Get and handle opcode
    if   (block["info"]["category"] == "variables") and (block["info"]["shape"] == "reporter"):
        opcode = "special_variable_value"
    elif (block["info"]["category"] == "list"     ) and (block["info"]["shape"] == "reporter"):
        opcode = "special_list_value"
    else:
        if "id" not in block["info"]:
            raise ValueError(f"Couldn't recognize block with shape {repr(spec)}")
        opcode: str = block["info"]["id"]
    if opcode.startswith("sb2"):
        raise NotImplementedError("Scratch 2 is not supported. Please switch to Scratch 3.")
    
    if isStandardOpcode(opcode):
        opcode = opcode.lower()
    elif "." in opcode:
        opcode = opcode.split(".")[0] + "_" + ".".join(opcode.split(".")[1:])
    
    category = opcode.split("_")[0]
    rest     = "_".join(opcode.split("_")[1:])
    if category == "operators": category = "operator"
    opcode: str = category + "_" + rest

    # handle opcode exceptions
    if   opcode == "looks_nextbackdrop_block": opcode = "looks_nextbackdrop"
    elif opcode == "control_if":
        if len(arguments) == 2: pass # Keep the opcode
        if len(arguments) == 3: opcode = "control_if_else" # When there is an "else" arg
        
    argumentsInfo = getArgumentOrder(opcode=opcode)
    inputs  = {}
    options = {}
    for i, argumentValue in enumerate(arguments):
        argumentId, mode = argumentsInfo[i]
        if mode == "OPTION":
            if "text" not in argumentValue:
                raise ValueError("Can't convert block(s) to field argument.")
            options[argumentId] = argumentValue["text"]
        else:
            if   "block"  in argumentValue: inputs[argumentId] = {"block" : argumentValue["block" ]}
            if   "blocks" in argumentValue: inputs[argumentId] = {"blocks": argumentValue["blocks"]}
            elif "text"   in argumentValue: inputs[argumentId] = {"text"  : argumentValue["text"  ]}

    return {
        "opcode"   : getOptimizedOpcode(opcode),
        "inputs"   : inputs,
        "options"  : options,
    }

def convertBlocks(blocks):
    newBlocks = []
    for block in blocks:
        if "label" in block: continue # Skip, because "block" is a comment
        newBlocks.append(convertBlock(block))
    return newBlocks

newScripts = []
i = 0
for script in scripts:
    newBlocks = convertBlocks(script["blocks"])
    if newBlocks == []: continue
    newScripts.append({
        "position": [0, 1000*i],
        "blocks"  : newBlocks,
    })
    i += 1

pp(newScripts)
writeJSONFile("src/pypenguin/penguinblocks/opt.json", newScripts)

from pypenguin import compressProject
from pypenguin.utility import Platform
project = {"sprites": [{"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["jgJSON", "Bitwise"], "extensionURLs": {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}}
project["sprites"][0]["scripts"] = newScripts
writeJSONFile("project/project.json", project)

compressProject(
    optimizedProjectDir="project",
    projectFilePath="export.pmp",
    targetPlatform=Platform.PENGUINMOD,
    deoptimizedDebugFilePath="t_deop.json",
)
