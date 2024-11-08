exec("import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))")

from helper_functions import generateRandomToken, generateSelector, pp, ikv, flipKeysAndValues, WhatIsGoingOnError

from deoptimize.variables_lists import translateVariables, translateLists
from deoptimize.broadcasts import generateBroadcastTokens
from deoptimize.blocks_scripts import linkBlocksToScript, unnestScript
from deoptimize.costumes_sounds import translateCostumes, translateSounds
from deoptimize.comments import translateComment

from database import opcodeDatabase

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
        "variables" : variableTokens,
        "lists"     : listTokens,
        "broadcasts": broadcastTokens,
    }
    return tokens, translatedVariableDatas, translatedListDatas, monitorDatas

def deoptimizeProject(projectData):
    tokens, translatedVariableDatas, translatedListDatas, monitorDatas = generateTokens(data=projectData)    
    
    newSpriteDatas = []
    for spriteData in projectData["sprites"]:
        newCommentDatas = {}
        newSpriteBlocks = {}
        for scriptID, scriptData in enumerate(spriteData["scripts"]):
            linkedScriptData, scriptCommentDatasA = linkBlocksToScript(
                data=scriptData, 
                spriteName=spriteData["name"],
                tokens=tokens,
                scriptIDs=[scriptID],
            )
            
            unnestedScriptData, scriptCommentDatasB = unnestScript(
                data=linkedScriptData, 
                spriteName=spriteData["name"],
                tokens=tokens,
                scriptIDs=[scriptID],
            )
            scriptCommentDatas = scriptCommentDatasA | scriptCommentDatasB
            newCommentDatas |= scriptCommentDatas
            newSpriteBlocks |= unnestedScriptData
        nameKey = None if spriteData["isStage"] else spriteData["name"]
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = generateSelector(scriptIDs=[], index=i, isComment=True)
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
    
