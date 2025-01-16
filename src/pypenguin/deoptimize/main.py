from pypenguin.utility import BlockSelector, stringToToken, Platform, pformat, pp, writeJSONFile, readJSONFile

from pypenguin.deoptimize.variables_lists import translateVariables, translateLists
from pypenguin.deoptimize.blocks_scripts import prepareScripts, flattenScripts, restoreBlocks, unprepareBlocks, makeJsonCompatible
from pypenguin.deoptimize.broadcasts import generateBroadcasts
from pypenguin.deoptimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin.deoptimize.comments import translateComment
from pypenguin.deoptimize.monitors import translateMonitor
from pypenguin.deoptimize.scratch_adaption import adaptProject
from pypenguin.deoptimize.precompilation import exportBlocks, findMatchingScript
from pypenguin.database import deoptimizeOptionValue

import os

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

def deoptimizeProject(projectData, targetPlatform):
    if os.path.exists("precompiled.json"):
        precompiledScriptDatas = readJSONFile("precompiled.json")
    else:
        precompiledScriptDatas = []
    translatedVariableDatas, translatedListDatas = translateVariablesLists(data=projectData)    
    broadcastDatas = generateBroadcasts(data=projectData["sprites"])
    
    newSpriteDatas  = []
    exportedScripts = []
    for i, spriteData in enumerate(projectData["sprites"]):
        for scriptData in spriteData["scripts"]:
            print(200*"/")
            pp(scriptData)
            print(findMatchingScript(scriptData, precompiledScriptDatas))
        
        preparedScriptDatas = prepareScripts(spriteData["scripts"])
        flattendScriptDatas = flattenScripts(preparedScriptDatas)
        spriteName = None if spriteData["isStage"] else spriteData["name"]
        newSpriteBlockDatas, scriptCommentDatas = restoreBlocks(
            data=flattendScriptDatas,
            spriteName=spriteName,
        )
        newCommentDatas = scriptCommentDatas
        
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = BlockSelector()
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=None,
            )
        newSpriteBlockDatas = unprepareBlocks(
            data=newSpriteBlockDatas,
        )
        exportedScripts += exportBlocks(
            data=newSpriteBlockDatas, 
            commentDatas=newCommentDatas, 
            optimizedScriptDatas=spriteData["scripts"],
        )
        if i == 1:
            pass#with open("s_pre.txt", "w") as file:
            #    file.write((pformat((newSpriteBlockDatas, newCommentDatas))))
            #with open("s_mid.txt", "w") as file:
            #    file.write((pformat(exportedScripts[1])))
            #loadedScript = loadScript(data=exportedScripts[1], spriteName=spriteData["name"])
            #with open("s_aft.txt", "w") as file:
            #    file.write((pformat(loadedScript)))

        
        newSpriteBlockDatas, newCommentDatas = makeJsonCompatible(
            data=newSpriteBlockDatas,
            commentDatas=newCommentDatas,
            targetPlatform=targetPlatform,
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
            "variables"     : translatedVariableDatas[spriteName],
            "lists"         : translatedListDatas    [spriteName],
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
            if projectData.get("textToSpeechLanguage", None) == None:
                newTextToSpeechLanguage = None
            else:
                newTextToSpeechLanguage = deoptimizeOptionValue(
                    optionType="text to speech language",
                    optionValue=["value", projectData["textToSpeechLanguage"]]
                ) # eg. "English (en)" -> "en"
            newSpriteData |= {
                "broadcasts"          : broadcastDatas,
                "layerOrder"          : 0,
                "tempo"               : projectData.get("tempo", 60),
                "videoTransparency"   : projectData.get("videoTransparency", 50),
                "videoState"          : projectData.get("videoState", "on"),
                "textToSpeechLanguage": newTextToSpeechLanguage,
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
    
    writeJSONFile("precompiled.json", exportedScripts)    
    
    # Translate monitors
    newMonitorDatas = []
    for monitorData in projectData["monitors"]:
        newMonitorDatas.append(translateMonitor(data=monitorData))

    newProjectData = {
        "targets"      : newSpriteDatas,
        "monitors"     : newMonitorDatas,
        "extensionData": projectData.get("extensionData", {}),
        "extensions"   : projectData["extensions"],    
        "extensionURLs": projectData.get("extensionURLs", {}),
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
        "credit": "Made using https://github.com/Fritzforcode/PyPenguin",
    }
    if targetPlatform == Platform.SCRATCH:
        newProjectData = adaptProject(newProjectData)
    return newProjectData
    
