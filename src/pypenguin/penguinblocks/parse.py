import subprocess, json, shutil, sys, shlex, json
from pypenguin.utility import readJSONFile, writeJSONFile, pp, generateCustomOpcode
from pypenguin.database import getArgumentOrder, getOptimizedOpcode, autocompleteOptionValue, getInputType, getOptionType, getOptionValueDefault

COMMENT_X_OFFSET = 400
COMMENT_SIZE = [200, 80]
COMMENT_Y_PADDING = 20
COMMENT_IS_MINIMIZED = False

variables = []
lists     = []

def convertBlock(block):
    global variables, lists
    def isStandardOpcode(opcode) -> bool:
        return bool(opcode) and all(char.isupper() or char == '_' or char.isdigit() for char in opcode)
    
    # Handle comment
    
    comment = None
    specification = {}
    if block["comment"] != None:
        commentText = block["comment"]["label"]["value"]
        try:
            specification = json.loads(commentText)
        except json.JSONDecodeError:
            pass
        else:
            commentText = specification.get("comment", None)
        
        if commentText != None: 
            comment = {
                "position": None,
                "size": COMMENT_SIZE,
                "isMinimized": COMMENT_IS_MINIMIZED,
                "text": commentText,
            }

    # Get and handle opcode
    if "id" not in block["info"]:
        if   (block["info"]["category"] == "variables") and (block["info"]["shape"] == "reporter"):
            opcode = "special_variable_value"
        elif (block["info"]["category"] == "list"     ) and (block["info"]["shape"] == "reporter"):
            opcode = "special_list_value"
        elif (block["info"]["category"] == "custom"   ) and (block["info"]["selector"] == "call" ):
            opcode = "procedures_call"
        else:
            raise ValueError(f"Couldn't recognize block with shape {repr(block['info']['hash'])}")
    else:
        opcode: str = block["info"]["id"]
    if opcode.startswith("sb2"):
        raise NotImplementedError("Scratch 2 is not supported. Please switch to Scratch 3.")
    
    if   isStandardOpcode(opcode):
        opcode = opcode.lower()
    elif opcode == "scratchblocks:end":
        return None
    elif "." in opcode:
        opcode = opcode.split(".")[0] + "_" + ".".join(opcode.split(".")[1:])
    
    category = opcode.split("_")[0]
    rest     = "_".join(opcode.split("_")[1:])
    if category == "operators": category = "operator"
    opcode: str = category + "_" + rest
    
    if opcode in {"procedures_definition", "procedures_call"}:
        customOpcode = generateCustomOpcode(
            proccode=block["info"]["call"],
            argumentNames=block["info"]["names"],
        )
        
        if opcode == "procedures_definition":
            noScreenRefresh = specification.get("noScreenRefresh", True)
            blockType       = specification.get("blockType", "instruction")
            newBlock = {
                "opcode": getOptimizedOpcode("special_define"),
                "inputs": {},
                "options": {
                    "noScreenRefresh": ["value", noScreenRefresh],
                    "customOpcode"   : ["value", customOpcode   ],
                    "blockType"      : ["value", blockType      ],
                },
            }
            if comment != None: newBlock["comment"] = comment
            return newBlock
            
    arguments = []
    for child in block["children"]:
        if   "info" in child: # An input block
            if child["info"]["shape"] == "outline": continue # skip e.g. used in custom blocks
            arguments.append({
                "kind": "block", 
                "value": convertBlock(child),
            })
        elif "blocks" in child: # A blocks substack input
            arguments.append({
                "kind": "blocks",
                "value": convertBlocks(child["blocks"]),
            })
        elif "shape" in child: # An input or option literal
            arguments.append({
                "kind": "text",
                "value": child["value"] if child["shape"] != "boolean" else None
            })

    # handle opcode exceptions
    if   opcode == "looks_nextbackdrop_block": opcode = "looks_nextbackdrop"
    elif opcode == "control_if":
        if len(arguments) == 2: pass # Keep the opcode
        if len(arguments) == 3: opcode = "control_if_else" # When there is an "else" ar

    if opcode == "procedures_call":
        argumentsInfo = []
        for argumentName in block["info"]["names"]:
            if   ("(" + argumentName + ")") in customOpcode:
                argumentsInfo.append([argumentName, "block-and-text"])
            elif ("<" + argumentName + ">") in customOpcode:
                argumentsInfo.append([argumentName, "block-only"])
            else: raise Exception()
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
                optionType = getInputType(opcode=opcode, inputId=argumentId) # input type is substituted for block-and-option inputs
                if   argumentKind == "block":
                    inputValue = {
                        "option": getOptionValueDefault(optionType=optionType),
                        "block" : argumentValue,
                    }
                elif argumentKind == "text":
                    inputValue = {
                        "option": autocompleteOptionValue(optionValue=argumentValue, optionType=optionType),
                    }
                inputs [argumentId] =  inputValue
        
    if   opcode == "special_variable_value":
        name = block["info"]["hash"]
        variables.append(name)
        options["VARIABLE"] = autocompleteOptionValue(optionValue=name, optionType="variable")
    elif opcode == "special_list_value":
        name = block["info"]["hash"]
        lists.append(name)
        options["LIST"    ] = autocompleteOptionValue(optionValue=name, optionType="list"    )
    elif opcode == "procedures_call":
        options["customOpcode"] = ["value", customOpcode]
    
    newBlock = {
        "opcode"   : getOptimizedOpcode(opcode),
        "inputs"   : inputs,
        "options"  : options,
    }
    if comment != None: newBlock["comment"] = comment
    return newBlock

def convertBlocks(blocks):
    newBlocks = []
    for block in blocks:
        if "label" in block: continue # Skip, because "block" is a comment
        newBlock = convertBlock(block)
        if newBlock == None: continue
        newBlocks.append(newBlock)
    return newBlocks

def finishBlock(block, scriptPos, commentCounter):
    if "comment" in block:
        block["comment"]["position"] = [
            scriptPos[0] + COMMENT_X_OFFSET,
            scriptPos[1] + commentCounter * (COMMENT_SIZE[1] + COMMENT_Y_PADDING),
        ]
        commentCounter += 1
    if "inputs" in block:
        for inputId, inputValue in block["inputs"].items():
            if "block" in inputValue:
                commentCounter = finishBlock(
                    inputValue["block"],
                    scriptPos=scriptPos,
                    commentCounter=commentCounter,
                )
            if "blocks" in inputValue:
                commentCounter = finishBlocks(
                    inputValue["blocks"],
                    scriptPos=scriptPos,
                    commentCounter=commentCounter,
                )
    return commentCounter

def finishBlocks(blocks, scriptPos, commentCounter=0):
    for block in blocks:
        commentCounter = finishBlock(
            block, 
            scriptPos=scriptPos, 
            commentCounter=commentCounter
        )
    return commentCounter

def parseBlockText(blockText: str):
    jsPath     = "src/pypenguin/penguinblocks/main.js"
    outputPath = "src/pypenguin/penguinblocks/in.json"

    ## On Windows/Linux
    #"""Check if Node.js is installed and accessible."""
    #if not shutil.which("node"):
    #    print("Error: Node.js is not installed or not in PATH.")
    #    print("Download it from https://nodejs.org/")
    #    sys.exit(1)
    #
    ## Run the JavaScript file with arguments using Node.js
    #result = subprocess.run(
    #    ["node", jsPath, blockText, outputPath],
    #    capture_output=True,
    #    text=True,
    #)
    #if result.returncode == 0:
    #    if result.stdout != "": # When it isn't empty
    #        print("JavaScript output:", result.stdout)
    #else:
    #    print("Error:", result.stderr)



    # On other operating systems      
    print(shlex.join(["node", jsPath, blockText, outputPath]))
    input()

    
    
    
    scripts = readJSONFile(outputPath, ensurePath=True)["scripts"]
    
    newScripts = []
    for i, script in enumerate(scripts):
        scriptPos = [0, 1000*i]
        newBlocks = convertBlocks(script["blocks"])
        if newBlocks == []: continue
        
        finishBlocks(newBlocks, scriptPos=scriptPos)
        newScripts.append({
            "position": scriptPos,
            "blocks"  : newBlocks,
        })
    return newScripts
    
if __name__ == "__main__":
    blockText = """
    ...
    """

    newScripts = parseBlockText(blockText)

    writeJSONFile("src/pypenguin/penguinblocks/opt.json", newScripts)
    
    from pypenguin import compressProject, validateProject
    from pypenguin.utility import Platform
    project = {"sprites": [
        {"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}, 
        {"name": "main", "isStage": False, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100, "layerOrder": 1, "visible": True, "position": [0, 0], "size": 100, "direction": 90, "draggable": True, "rotationStyle": "all around", "localVariables": [], "localLists": []}
    ], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["pen"], "extensionURLs": {}}
    
    project["sprites"][1]["scripts"] = newScripts
    project["globalVariables"] = [{"name": variable, "currentValue": "", "isCloudVariable": False} for variable in variables]
    project["globalLists"    ] = [{"name": list    , "currentValue": []} for list in lists]
    writeJSONFile("project/project.json", project)
    validateProject(project)
    compressProject(
        optimizedProjectDir="project",
        projectFilePath="export.sb3",
        targetPlatform=Platform.SCRATCH,
        deoptimizedDebugFilePath="t_deop.json",
    )
    