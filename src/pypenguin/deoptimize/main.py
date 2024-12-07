from pypenguin.helper_functions import newTempSelector, pp, stringToToken

from pypenguin.deoptimize.variables_lists import translateVariables, translateLists
from pypenguin.deoptimize.blocks_scripts import restoreScripts, flattenScripts, restoreBlocks, finishBlocks
from pypenguin.deoptimize.broadcasts import generateBroadcasts
from pypenguin.deoptimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin.deoptimize.comments import translateComment
from pypenguin.deoptimize.monitors import translateMonitor

def translateVariablesLists(data):
    spriteNames = [sprite["name"] for sprite in data["sprites"]][1:]
    translatedVariableDatas = translateVariables(
        data=data, 
        spriteNames=spriteNames,
    )
    translatedListDatas = translateLists(
        data=data, 
        spriteNames=spriteNames,
    )
    return translatedVariableDatas, translatedListDatas

def deoptimizeProject(projectData):
    spriteNames = [sprite["name"] for sprite in projectData["sprites"]][1:]
    translatedVariableDatas, translatedListDatas = translateVariablesLists(data=projectData)    
    broadcastDatas = generateBroadcasts(data=projectData["sprites"])
    
    newSpriteDatas = []
    for i, spriteData in enumerate(projectData["sprites"]):
        restoredScriptDatas = restoreScripts(spriteData["scripts"])
        flattendScriptDatas   = flattenScripts(restoredScriptDatas)
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

        if i == 0:
            token = stringToToken("_stage_")
        else:
            token = stringToToken(spriteData["name"])
        
        
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
            "id"            : token,
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
    
    # Translate monitors
    newMonitorDatas = []
    for monitorData in projectData["monitors"]:
        newMonitorDatas.append(translateMonitor(data=monitorData))

    newProjectData = {
        "targets"      : newSpriteDatas,
        "monitors"     : newMonitorDatas,
        "extensionData": projectData["extensionData"],
        "extensions"   : projectData["extensions"],
        "meta"         : {
            "semver": "3.0.0",
            "vm"    : "0.2.0",
            "agent" : "",
            "platform": {
                "name"   : "PenguinMod",
                "url"    : "https://penguinmod.com/",
                "version": "stable",
            },
        }, # Hardcoded because there is no use in changing it
    }
    return newProjectData
    
