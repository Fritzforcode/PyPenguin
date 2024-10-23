exec("import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))")

from helper_functions import readJSONFile, writeJSONFile, pp, ikv, WhatIsGoingOnError

from costumes_sounds import translateCostumes, translateSounds
from variables_lists import translateVariables, translateLists
from blocks_scripts import translateScript, generateBlockChildrenPs
from comments import translateComment

opcodeDatabase = readJSONFile("assets/opcode_database.jsonc")


def optimizeProject(sourcePath, targetPath):
    dataSource = readJSONFile(sourcePath)
    newSpriteDatas = []
    for i, spriteData in enumerate(dataSource["targets"]):
        commentDatas = spriteData["comments"]
        floatingCommentDatas = [] # The comments that aren't connected to any blocks
        for commentData in commentDatas.values():
            if commentData["blockId"] == None: # No Block connection
                floatingCommentDatas.append(translateComment(data=commentData))
        ancestorPs, blockChildrenPs = generateBlockChildrenPs(data=spriteData["blocks"])
        newScriptDatas = []
        for ancestorP in ancestorPs:
            newScriptData = translateScript(
                data=spriteData["blocks"], 
                ancestorP=ancestorP, 
                blockChildrenPs=blockChildrenPs,
                commentDatas=commentDatas,
            )
            newScriptDatas.append(newScriptData)
        translatedCostumeDatas = translateCostumes(data=spriteData["costumes"])
        translatedSoundDatas   = translateSounds  (data=spriteData["sounds"])
        newSpriteData = {
            "isStage"       : i == 0,
            "name"          : spriteData["name"],
            "scripts"       : newScriptDatas,
            "comments"      : floatingCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : translatedCostumeDatas,
            "sounds"        : translatedSoundDatas,
            "volume"        : spriteData["volume"],
            "layerOrder"    : spriteData["layerOrder"],
        }
        if spriteData["isStage"]:
            newSpriteData |= {
                "tempo"               : spriteData["tempo"],
                "videoTransparency"   : spriteData["videoTransparency"],
                "videoState"          : spriteData["videoState"],
                "textToSpeechLanguage": spriteData["textToSpeechLanguage"],
            }
        else:
            newSpriteData |= {
                "visible"      : spriteData["visible"],
                "position"     : [spriteData["x"], spriteData["y"]],
                "size"         : spriteData["size"],
                "direction"    : spriteData["direction"],
                "draggable"    : spriteData["draggable"],
                "rotationStyle": spriteData["rotationStyle"],
            }
        newSpriteDatas.append(newSpriteData)
    newData = {
        "sprites"      : newSpriteDatas,
        "variables"    : translateVariables(
            data=dataSource["targets"], 
            monitorDatas=dataSource["monitors"],
        ),
        "lists"        : translateLists(
            data=dataSource["targets"],
            monitorDatas=dataSource["monitors"],
        ),
        "extensionData": dataSource["extensionData"],
        "extensions"   : dataSource["extensions"],
        "meta"         : dataSource["meta"],
    }
    writeJSONFile(targetPath, newData)

optimizeProject(
    sourcePath="assets/studies/typeTest.json", 
    targetPath="assets/optimized.json",
)
