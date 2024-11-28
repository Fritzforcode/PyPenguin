from pypenguin.helper_functions import generateRandomToken,  tempSelector, pp, ikv, flipKeysAndValues, WhatIsGoingOnError

from pypenguin.deoptimize.variables_lists import translateVariables, translateLists
from pypenguin.deoptimize.broadcasts import generateBroadcastTokens
from pypenguin.deoptimize.blocks_scripts import unfinishScripts, flattenScripts, restoreBlocks, finishBlocks
from pypenguin.deoptimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin.deoptimize.comments import translateComment

def generateTokens(data):
    spriteNames = [sprite["name"] for sprite in data["sprites"]][1:]
    translatedVariableDatas, variableTokens, variableMonitorDatas = translateVariables(
        data=data, 
        spriteNames=spriteNames,
    )
    translatedListDatas, listTokens, listMonitorDatas = translateLists(
        data=data, 
        spriteNames=spriteNames,
    )
    monitorDatas = variableMonitorDatas + listMonitorDatas
    broadcastTokens = generateBroadcastTokens(
        data=data["sprites"],
        spriteNames=spriteNames,
    )
    tokens = {
        "variables"   : variableTokens,
        "lists"       : listTokens,
        "broadcasts"  : broadcastTokens,
    }
    return tokens, translatedVariableDatas, translatedListDatas, monitorDatas

def deoptimizeProject(projectData):
    tokens, translatedVariableDatas, translatedListDatas, monitorDatas = generateTokens(data=projectData)    
    
    newSpriteDatas = []
    for spriteData in projectData["sprites"]:
        newCommentDatas       = {}
        newSpriteBlockDatas   = {}
        
        unfinishedScriptDatas = unfinishScripts(spriteData["scripts"])
        flattendScriptDatas   = flattenScripts(unfinishedScriptDatas)
        restoredBlockDatas    = restoreBlocks(
            data=flattendScriptDatas,
            spriteName=spriteData["name"],
            tokens=tokens,
        )

        scriptCommentDatas    = {}#scriptCommentDatasA | scriptCommentDatasB
        newCommentDatas      |= scriptCommentDatas
        newSpriteBlockDatas  |= restoredBlockDatas
        
        nameKey = None if spriteData["isStage"] else spriteData["name"]
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = tempSelector(path=[i]+["c"])
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=None,
            )
        newSpriteBlockDatas, newCommentDatas = finishBlocks(
            data=newSpriteBlockDatas,
            commentDatas=newCommentDatas,
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
            "blocks"        : newSpriteBlockDatas,
            "comments"      : newCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : newCostumeDatas,
            "sounds"        : newSoundDatas,
            "id"            : generateRandomToken(),
            "volume"        : spriteData["volume"],
        }
        if spriteData["isStage"]:
            newSpriteData["broadcasts"] = flipKeysAndValues(tokens["broadcasts"][None])
            newSpriteData |= {
                "layerOrder"          : 0,
                "tempo"               : projectData["tempo"],
                "videoTransparency"   : projectData["videoTransparency"],
                "videoState"          : projectData["videoState"],
                "textToSpeechLanguage": projectData["textToSpeechLanguage"],
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
                "layerOrder"   : spriteData["layerOrder"],
            }
        newSpriteDatas.append(newSpriteData)
    newProjectData = {
        "targets"      : newSpriteDatas,
        "monitors"     : monitorDatas,
        "extensionData": projectData["extensionData"],
        "extensions"   : projectData["extensions"],
        "meta"         : projectData["meta"],
    }
    return newProjectData
    
