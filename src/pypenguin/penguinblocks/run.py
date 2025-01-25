import subprocess
from pypenguin.utility import readJSONFile, writeJSONFile, pp
from pypenguin.database import getArgumentOrder, getOptimizedOpcode, autocompleteOptionValue, getInputType, getOptionType, getOptionValueDefault

variables = []
lists     = []

def convertBlock(block):
    global variables, lists
    def isStandardOpcode(opcode) -> bool:
        return bool(opcode) and all(char.isupper() or char == '_' or char.isdigit() for char in opcode)
    arguments = []
    spec = "" # used for unrecognized blocks eg. "shout _" for "shout (Hi)"
    for child in block["children"]:
        if   "info" in child: # An input block
            if child["info"]["shape"] == "outline": continue # skip e.g. used in custom blocks
            arguments.append({
                "kind": "block", 
                "value": convertBlock(child),
            })
            spec += " [ARG]"
        elif "blocks" in child: # A blocks substack input
            arguments.append({
                "kind": "blocks",
                "value": convertBlocks(child["blocks"]),
            })
            spec += " [SUBSTACK]"
        elif "shape" in child: # An input or option literal
            arguments.append({
                "kind": "text",
                "value": child["value"] if child["shape"] != "boolean" else None
            })
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
        if len(arguments) == 3: opcode = "control_if_else" # When there is an "else" ar

    if opcode == "procedures_definition":
        pp(block)
    else:
        argumentsInfo = getArgumentOrder(opcode=opcode)
        inputs  = {}
        options = {}
        for i, argument in enumerate(arguments):
            argumentId, mode = argumentsInfo[i]
            argumentKind  = argument["kind" ]
            argumentValue = argument["value"]
            match mode:
                case "OPTION":
                    assert argumentKind == "text", "Can't convert block or substack argument to field dropdown."
                    optionType = getOptionType(opcode=opcode, optionId=argumentId)
                    options[argumentId] = autocompleteOptionValue(optionValue=argumentValue, optionType=optionType)
                    if   optionType == "variable": variables.append(argumentValue)
                    elif optionType == "list"    : lists    .append(argumentValue)
                case "block-and-text"|"block-and-menu-text":
                    assert argumentKind in {"block", "text"}, "Can't convert substack argument to a block-or-text input."
                    inputs [argumentId] = {argumentKind: argumentValue} # Trick to simplify code kind is either "block" or "text"
                case "block-only":
                    assert argumentKind == "block", "Can't convert substack/text argument to a block-only input."
                    inputs [argumentId] = {"block": argumentValue}
                case "script":
                    assert argumentKind == "blocks", "Can't convert block/text argument to a substack input."
                    inputs [argumentId] = {"blocks": argumentValue}
                case "block-and-option"|"block-and-broadcast-option":
                    assert argumentKind in {"block", "text"}, "Can't convert substack argument to a block-or-option input."
                    if   argumentKind == "block":
                        inputValue = {
                            "option": getOptionValueDefault(optionType=optionType),
                            "block" : argumentValue,
                        }
                    elif argumentKind == "text":
                        optionType = getInputType(opcode=opcode, inputId=argumentId) # input type is substituted for block-and-option inputs
                        inputValue = {
                            "option": autocompleteOptionValue(optionValue=argumentValue, optionType=optionType),
                        }
                    inputs [argumentId] =  inputValue
        
    newOpcode = None
    if   opcode == "special_variable_value":
        name = block["info"]["hash"]
        variables.append(name)
        options["VARIABLE"] = autocompleteOptionValue(optionValue=name, optionType="variable")
    elif opcode == "special_list_value":
        name = block["info"]["hash"]
        lists.append(name)
        options["LIST"    ] = autocompleteOptionValue(optionValue=name, optionType="list"    )

    elif opcode == "procedures_definition":
        newOpcode = "special_define"

    return {
        "opcode"   : getOptimizedOpcode(opcode) if newOpcode==None else newOpcode,
        "inputs"   : inputs,
        "options"  : options,
    }

def convertBlocks(blocks):
    newBlocks = []
    for block in blocks:
        if "label" in block: continue # Skip, because "block" is a comment
        newBlocks.append(convertBlock(block))
    return newBlocks

# Define the code string and output file path
code1 = """
when gf clicked
delete all of [screen data v]
repeat ((grid x size) * (grid y size)
 add (pick random (0) to (1)) to [screen data v]
end
set [tile size v] to (8)
set [grid x size v] to (50)
set [grid y size v] to (50)
forever
 erase all
end"""
code="""
define Render (x) asd <b>
set [# v] to (0)
go to x: (0) y: (0)
go to x: ((((grid x size) / (2)) * (tile size)) * (-1)) y: ((((grid y size) / (2)) * (tile size)) * (-1))
repeat (grid y) 
 repeat (grid x)
  change [# v] by (1)
  switch costume to (item (#) of [screen data v])
  stamp
  change x by (tile size)
 end
  change x by (((grid x size) * (tile size)) * (-1))
  change y  by (tile size)
end
"""

""" Draft Example
// env:extensions=["JSON"]
// env:sprite=Cat
// env:spritePos=[0,0]
// var:"abc"="hi"
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

from pypenguin import compressProject, validateProject
from pypenguin.utility import Platform
project = {"sprites": [{"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["pen"], "extensionURLs": {}}
project["sprites"][0]["scripts"] = newScripts
project["globalVariables"] = [{"name": variable, "currentValue": "", "isCloudVariable": False} for variable in variables]
project["globalLists"    ] = [{"name": list    , "currentValue": []} for list in lists]
writeJSONFile("project/project.json", project)
validateProject(project)
compressProject(
    optimizedProjectDir="project",
    projectFilePath="export.pmp",
    targetPlatform=Platform.PENGUINMOD,
    deoptimizedDebugFilePath="t_deop.json",
)
