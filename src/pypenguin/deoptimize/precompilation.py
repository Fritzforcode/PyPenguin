import json
from enum import Enum
from pypenguin.helper_functions import pp, replaceSelectors

class PathConstant(Enum):
    CB_DEFINITION_PATH     = json.dumps(["blocks", 0, "CB_DEFINITION"])
    CB_PROTOTYPE_PATH      = json.dumps(["blocks", 0, "CB_PROTOTYPE" ])
    CB_PROTOTYPE_ARGS      = "CB_PROTOTYPE_ARGS"
    
    CB_NEW_PATH            = json.dumps(["blocks", 0])
    CB_NEW_DEFINITION_PATH = json.dumps(["blocks", 0, "definition"])
    CB_NEW_PROTOTYPE_PATH  = json.dumps(["blocks", 0, "prototype" ])
    CB_NEW_PROTOTYPE_ARGS  = "args"
    
def convertScripts(data):
    pp(data)
    scripts = []
    for blockID, blockData in data.items():
        path = blockData["_placementPath_"]
        del blockData["_placementPath_"]
        scriptIndex, path = path[0], path[1:]
        pathString = json.dumps(path)
        
        print(scriptIndex, path, pathString)
        while len(scripts) <= scriptIndex:
            scripts.append({"blocks": {}, "table": {}})
        
        scripts[scriptIndex]["blocks"][pathString] = blockData
        scripts[scriptIndex]["table" ][blockID   ] = pathString
    
    pp(scripts)
    for script in scripts:
        # Combine blocks needed for a custom block definition
        if (PathConstant.CB_DEFINITION_PATH.value in script["blocks"]
        and PathConstant.CB_PROTOTYPE_PATH.value  in script["blocks"]):
            newDefinition = {
                "definition": script["blocks"][PathConstant.CB_DEFINITION_PATH.value],
                "prototype" : script["blocks"][PathConstant.CB_PROTOTYPE_PATH .value],
                "args"      : {},
            }
            del script["blocks"][PathConstant.CB_DEFINITION_PATH.value]
            del script["blocks"][PathConstant.CB_PROTOTYPE_PATH .value]
            
            for pathString, block in script["blocks"].copy().items():
                path = json.loads(pathString) # eg. '["blocks", 0, "CB_PROTOTYPE_ARGS", "my argument"]'
                # search for arguments of the custom block definition
                if path[-2] == PathConstant.CB_PROTOTYPE_ARGS.value:
                    newDefinition["args"][path[-1]] = blockData
                    del script["blocks"][pathString]
            
            # update translation table, because some paths have changed
            for blockSelector, pathString in script["table"].items():
                match pathString:
                    case PathConstant.CB_DEFINITION_PATH.value:
                        newPathString = PathConstant.CB_NEW_DEFINITION_PATH.value
                    case PathConstant.CB_PROTOTYPE_PATH.value :
                        newPathString = PathConstant.CB_NEW_PROTOTYPE_PATH .value
                    case _:
                        path = json.loads(pathString)
                        if path[-2] == PathConstant.CB_PROTOTYPE_ARGS.value:
                            newPath = path
                            newPath[-2] = PathConstant.CB_NEW_PROTOTYPE_ARGS.value
                            newPathString = json.dumps(newPath)
                        else: newPathString = pathString
                script["table"][blockSelector] = newPathString
            
            script["blocks"][PathConstant.CB_NEW_PATH.value] = newDefinition     
                
        # Replace remaining block selectors with paths
        #script["blocks"] = replaceSelectors(script["blocks"], table=None)
        table = {selector:{"_selector_": True, "path": pathString} for selector, pathString in script["table"].items()}
        script["blocks"] = replaceSelectors(script["blocks"], table=table)
        
        # Sort for consistency
        script["blocks"] = dict(sorted(script["blocks"].items()))
    pp(scripts)


