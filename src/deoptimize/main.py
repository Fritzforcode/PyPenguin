exec("import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))")

from helper_functions import readJSONFile, writeJSONFile, generateRandomToken, generateSelector, pp, ikv, flipKeysAndValues, WhatIsGoingOnError

from variables_lists import translateVariables, translateLists
from broadcasts import generateBroadcastTokens
from blocks_scripts import linkBlocksToScript, unnestScript
from costumes_sounds import translateCostumes, translateSounds
from comments import translateComment

opcodeDatabase = readJSONFile("assets/opcode_database.jsonc")

def generateTokens(data):
    spriteNames = [sprite["name"] for sprite in data["sprites"]][1:]
    translatedVariableDatas, variableTokens, variableMonitorDatas = translateVariables(
        data=data["variables"], 
        spriteNames=spriteNames,
    )
    translatedListDatas, listTokens, listMonitorDatas = translateLists(
        data=data["lists"], 
        spriteNames=spriteNames,
    )
    monitorDatas = variableMonitorDatas + listMonitorDatas
    broadcastTokens = generateBroadcastTokens(
        data=data["sprites"],
        spriteNames=spriteNames,
    )
    tokens = {
        "variables" : variableTokens,
        "lists"     : listTokens,
        "broadcasts": broadcastTokens,
    }
    return tokens, translatedVariableDatas, translatedListDatas, monitorDatas

def deoptimizeProject(sourcePath, targetPath):
    data = readJSONFile(sourcePath)
    tokens, translatedVariableDatas, translatedListDatas, monitorDatas = generateTokens(data=data)    
    
    newSpriteDatas = []
    for spriteData in data["sprites"]:
        newCommentDatas = {}
        newSpriteBlocks = {}
        for scriptID, scriptData in enumerate(spriteData["scripts"]):
            linkedScriptData, scriptCommentDatasA = linkBlocksToScript(
                data=scriptData, 
                spriteName=spriteData["name"],
                tokens=tokens,
                scriptID=scriptID,
            )
            
            unnestedScriptData, scriptCommentDatasB = unnestScript(
                data=linkedScriptData, 
                spriteName=spriteData["name"],
                tokens=tokens,
                scriptID=scriptID,
            )
            scriptCommentDatas = scriptCommentDatasA | scriptCommentDatasB
            newCommentDatas |= scriptCommentDatas
            newSpriteBlocks |= unnestedScriptData
        nameKey = None if spriteData["isStage"] else spriteData["name"]
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = generateSelector(scriptID=None, index=i, isComment=True)
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=None,
            )
        
        newCostumeDatas = translateCostumes(
            data=spriteData["costumes"],
        )
        newSoundDatas = translateSounds(
            data=spriteData["sounds"],
        )
        
        
        newSpriteData = {
            "isStage"       : spriteData["isStage"],
            "name"          : spriteData["name"],
            "variables"     : translatedVariableDatas[nameKey],
            "lists"         : translatedListDatas    [nameKey],
            "broadcasts"    : {},
            "customVars"    : [], # NO MEANING FOUND
            "blocks"        : newSpriteBlocks,
            "comments"      : newCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : newCostumeDatas,
            "sounds"        : newSoundDatas,
            "id"            : generateRandomToken(),
            "volume"        : spriteData["volume"],
            "layerOrder"    : spriteData["layerOrder"],
        }
        if spriteData["isStage"]:
            newSpriteData["broadcasts"] = flipKeysAndValues(broadcastTokens[None])
            newSpriteData |= {
                "tempo"               : spriteData["tempo"],
                "videoTransparency"   : spriteData["videoTransparency"],
                "videoState"          : spriteData["videoState"],
                "textToSpeechLanguage": spriteData["textToSpeechLanguage"],
            }
        else:
            newSpriteData |= {
                "visible"      : spriteData["visible"],
                "x"            : spriteData["position"][0],
                "y"            : spriteData["position"][1],
                "size"         : spriteData["size"],
                "direction"    : spriteData["direction"],
                "draggable"    : spriteData["draggable"],
                "rotationStyle": spriteData["rotationStyle"],
            }
        newSpriteDatas.append(newSpriteData)
    newProjectData = {
        "targets"      : newSpriteDatas,
        "monitors"     : monitorDatas,
        "extensionData": data["extensionData"],
        "extensions"   : data["extensions"],
        "meta"         : data["meta"],
    }
    #pp(newProjectData)
    writeJSONFile(targetPath, newProjectData)    


deoptimizeProject(sourcePath="assets/optimized.json", targetPath="asssets/deoptimized.json")
