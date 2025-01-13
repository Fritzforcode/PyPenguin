import json
from enum import Enum
from pypenguin.helper_functions import pp, replaceClasses, newTempSelector
from pypenguin.database import getBlockType

class PathConstant(Enum):
    CB_PROTOTYPE_ARGS      = "CB_PROTOTYPE_ARGS"
    
def convertScripts(data, commentDatas):
    pp(data)
    scripts = []
    for blockSelector, blockData in data.items():
        path = blockData["_placementPath_"]
        del blockData["_placementPath_"]
        scriptIndex, path = path[0], path[1:]
        pathString = json.dumps(path)
        
        while len(scripts) <= scriptIndex:
            scripts.append({"blocks": {}, "comments": {}, "table": {}})
        
        scripts[scriptIndex]["blocks"][pathString   ] = {"deoptimized": blockData, "doCompare": True}
        scripts[scriptIndex]["table" ][blockSelector] = pathString

        if blockData.get("comment") != None:
            commentPathString = json.dumps(path+["comment"])
            scripts[scriptIndex]["comments"][commentPathString   ] = commentDatas[blockData["comment"]]
            scripts[scriptIndex]["table"   ][blockData["comment"]] = commentPathString
            #blockData["comment"] = commentPathString
    
    pp(scripts)
    for scriptData in scripts:
        # Combine blocks needed for a custom block definition
         
        for pathString, blockData in scriptData["blocks"].items():
            oldOpcode = blockData["deoptimized"]["opcode"]
            blockType = getBlockType(opcode=oldOpcode, defaultNone=True)
            # Sign menu blocks and custom block definition prototype and args to not be compared later on. That is because these blocks do not exist in the optimized version
            doCompare = True
            if blockType == "menu" or oldOpcode == "procedures_prototype":
                doCompare = False
            if oldOpcode in ["argument_reporter_string_number", "argument_reporter_boolean"]:
                path = json.loads(pathString)
                if path[-2] == PathConstant.CB_PROTOTYPE_ARGS.value:
                    doCompare = False
            
            if not doCompare:
                blockData["doCompare"] = False

                

        # Replace remaining block selectors with paths
        table = {selector:{"_custom_": True, "_type_": "selector", "path": pathString} for selector, pathString in scriptData["table"].items()}

        def convertionFunc(obj):
            nonlocal table
            return table[obj]
        
        scriptData["blocks"  ] = replaceClasses(scriptData["blocks"  ], classes=[newTempSelector], convertionFunc=convertionFunc)
        scriptData["comments"] = replaceClasses(scriptData["comments"], classes=[newTempSelector], convertionFunc=convertionFunc)
        del scriptData["table"]
    
    #pp(scripts)


