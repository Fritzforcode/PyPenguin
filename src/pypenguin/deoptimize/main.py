from pypenguin.helper_functions import newTempSelector, stringToToken, Platform, pp

from pypenguin.deoptimize.variables_lists import translateVariables, translateLists
from pypenguin.deoptimize.blocks_scripts import prepareScripts, flattenScripts, restoreBlocks, unprepareBlocks
from pypenguin.deoptimize.broadcasts import generateBroadcasts
from pypenguin.deoptimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin.deoptimize.comments import translateComment
from pypenguin.deoptimize.monitors import translateMonitor
from pypenguin.deoptimize.scratch_adaption import adaptProject
from pypenguin.database import deoptimizeOptionValue

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
    translatedVariableDatas, translatedListDatas = translateVariablesLists(data=projectData)    
    broadcastDatas = generateBroadcasts(data=projectData["sprites"])
    
    newSpriteDatas = []
    for i, spriteData in enumerate(projectData["sprites"]):
        preparedScriptDatas = prepareScripts(spriteData["scripts"])
        flattendScriptDatas = flattenScripts(preparedScriptDatas)
        newSpriteBlockDatas, scriptCommentDatas = restoreBlocks(
            data=flattendScriptDatas,
            spriteName=spriteData["name"],
        )
        print(100*"#")
        #pp(flattendScriptDatas)
        #pp(newSpriteBlockDatas)
        newCommentDatas = scriptCommentDatas
        
        nameKey = None if spriteData["isStage"] else spriteData["name"]
        for i, commentData in enumerate(spriteData["comments"]):
            commentID = newTempSelector()
            newCommentDatas[commentID] = translateComment(
                data=commentData,
                id=None,
            )
        newSpriteBlockDatas, newCommentDatas = unprepareBlocks(
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
    
