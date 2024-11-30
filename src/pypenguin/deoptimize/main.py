from pypenguin.helper_functions import generateRandomToken,  newTempSelector, pp, ikv, flipKeysAndValues, WhatIsGoingOnError

from pypenguin.deoptimize.variables_lists import translateVariables, translateLists
from pypenguin.deoptimize.blocks_scripts import unfinishScripts, flattenScripts, restoreBlocks, finishBlocks
from pypenguin.deoptimize.broadcasts import generateBroadcasts
from pypenguin.deoptimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin.deoptimize.comments import translateComment

def translateVariablesLists(data):
    spriteNames = [sprite["name"] for sprite in data["sprites"]][1:]
    translatedVariableDatas, variableMonitorDatas = translateVariables(
        data=data, 
        spriteNames=spriteNames,
    )
    translatedListDatas, listMonitorDatas = translateLists(
        data=data, 
        spriteNames=spriteNames,
    )
    monitorDatas = variableMonitorDatas + listMonitorDatas
    return translatedVariableDatas, translatedListDatas, monitorDatas

def deoptimizeProject(projectData):
    spriteNames = [sprite["name"] for sprite in projectData["sprites"]][1:]
    translatedVariableDatas, translatedListDatas, monitorDatas = translateVariablesLists(data=projectData)    
    broadcastDatas = generateBroadcasts(data=projectData["sprites"])
    
    newSpriteDatas = []
    for spriteData in projectData["sprites"]:
        unfinishedScriptDatas = unfinishScripts(spriteData["scripts"])
        flattendScriptDatas   = flattenScripts(unfinishedScriptDatas)
        newSpriteBlockDatas, scriptCommentDatas = restoreBlocks(
            data=flattendScriptDatas,
            spriteName=spriteData["name"],
        )

        newCommentDatas = scriptCommentDatas
        
        nameKey = None if spriteData["isStage"] else spriteData["name"]
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = newTempSelector()
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=None,
            )
        newSpriteBlockDatas, newCommentDatas = finishBlocks(
            data=newSpriteBlockDatas,
            spriteName=spriteData["name"],
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
            newSpriteData |= {
                "broadcasts"          : broadcastDatas,
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
    
