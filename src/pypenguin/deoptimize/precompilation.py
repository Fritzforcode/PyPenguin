import json
from enum import Enum
from pypenguin.utility import editDataStructure, BlockSelector, LocalStringToToken, getDataAtPath
from pypenguin.database import getBlockType

class PathConstant(Enum):
    CB_PROTOTYPE_ARGS = "CB_PROTOTYPE_ARGS"
    
def exportScripts(data, commentDatas, optimizedScriptDatas):
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
    
    for scriptIndex, scriptData in enumerate(scripts):
        # Combine blocks needed for a custom block definition
         
        for pathString, blockData in scriptData["blocks"].items():
            path = json.loads(pathString)
            oldOpcode = blockData["deoptimized"]["opcode"]
            blockType = getBlockType(opcode=oldOpcode, defaultNone=True)
            # Sign menu blocks and custom block definition prototype and args to not be compared later on. That is because these blocks do not exist in the optimized version
            doCompare = True
            if blockType == "menu" or oldOpcode == "procedures_prototype":
                doCompare = False
            if oldOpcode in ["argument_reporter_string_number", "argument_reporter_boolean"]:
                if path[-2] == PathConstant.CB_PROTOTYPE_ARGS.value:
                    doCompare = False
            
            if not doCompare:
                blockData["doCompare"] = False
            if blockData.get("doCompare", True):
                blockData["optimized"] = getDataAtPath(data=optimizedScriptDatas, path=[scriptIndex]+path)
                

        # Replace remaining block selectors with paths
        table = {selector:{"_custom_": True, "_type_": "newTempSelector", "path": pathString} for selector, pathString in scriptData["table"].items()}

        def convertionFunc(obj):
            nonlocal table
            if isinstance(obj, blockSelector):
                return table[obj]
            if isinstance(obj, LocalStringToToken):
                return obj.toJSON()
        conditionFunc = lambda obj: isinstance(obj, (blockSelector, LocalStringToToken))
        scriptData["blocks"  ] = editDataStructure(scriptData["blocks"  ], conditionFunc=conditionFunc, convertionFunc=convertionFunc)
        scriptData["comments"] = editDataStructure(scriptData["comments"], conditionFunc=conditionFunc, convertionFunc=convertionFunc)
        del scriptData["table"]
    return scripts

def loadScript(data, spriteName):
    blockDatas   = data["blocks"  ]
    commentDatas = data["comments"]
    table = {itemPath: BlockSelector() for itemPath in (blockDatas|commentDatas).keys()}

    def convertionFunc(obj):
        nonlocal table, spriteName
        if obj["_type_"] == BlockSelector.__name__:
            return table[obj["path"]]
        if obj["_type_"] == LocalStringToToken.__name__:
            return LocalStringToToken(main=obj["main"], spriteName=spriteName)
        
    conditionFunc = lambda obj: (
        False if not isinstance(obj, dict) else (
            (obj.get("_custom_") == True) and ("_type_" in obj)
        )
    )
    blockDatas   = editDataStructure(blockDatas  , conditionFunc=conditionFunc, convertionFunc=convertionFunc)
    commentDatas = editDataStructure(commentDatas, conditionFunc=conditionFunc, convertionFunc=convertionFunc)
    newBlockDatas = {}
    for blockPath, blockData in blockDatas.items():
        newBlockDatas[table[blockPath]] = blockData["deoptimized"]
    newCommentDatas = {}
    for commentPath, commentData in commentDatas.items():
        newCommentDatas[table[commentPath]] = commentData
    return {"blocks": newBlockDatas, "comments": commentDatas}
    

def compareScript():
    pass

