from pypenguin.helper_functions         import pp, ikv

from pypenguin.optimize.costumes_sounds import translateCostumes, translateSounds
from pypenguin.optimize.variables_lists import translateVariables, translateLists
from pypenguin.optimize.blocks_scripts  import getCustomBlockMutations, prepareBlocks, nestScripts, finishScripts
from pypenguin.optimize.comments        import translateComment
from pypenguin.optimize.monitors        import translateMonitors

def optimizeProjectJSON(projectData):
    newSpriteDatas = []
    for i, spriteData in enumerate(projectData["targets"]):
        mutationDatas = getCustomBlockMutations(data=spriteData["blocks"])
        commentDatas = spriteData["comments"]
        floatingCommentDatas = [] # The comments that aren't connected to any blocks
        attachedCommentDatas = {}
        for j, commentID, commentData in ikv(commentDatas):
            if commentData["blockId"] == None: # No Block connection
                floatingCommentDatas.append(translateComment(data=commentData))
            else:
                attachedCommentDatas[commentID] = translateComment(data=commentData)
        
        preparedBlockDatas = prepareBlocks(
            data=spriteData["blocks"], 
            commentDatas=attachedCommentDatas,
            mutationDatas=mutationDatas,
        )
        nestedScriptDatas  = nestScripts  (data=preparedBlockDatas)
        newScriptDatas     = finishScripts(data=nestedScriptDatas)

        translatedCostumeDatas  = translateCostumes (data=spriteData["costumes"])
        translatedSoundDatas    = translateSounds   (data=spriteData["sounds"])
        translatedVariableDatas = translateVariables(data=spriteData)
        translatedListDatas     = translateLists    (data=spriteData)
        newSpriteData = {
            "isStage"       : i == 0,
            "name"          : spriteData["name"],
            "scripts"       : newScriptDatas,
            "comments"      : floatingCommentDatas,
            "currentCostume": spriteData["currentCostume"],
            "costumes"      : translatedCostumeDatas,
            "sounds"        : translatedSoundDatas,
            "volume"        : spriteData["volume"],
        }
        if spriteData["isStage"]:
            globalVariableDatas = translatedVariableDatas
            globalListDatas = translatedListDatas
        else:
            newSpriteData |= {
                "localVariables": translatedVariableDatas,
                "localLists"    : translatedListDatas,
                "layerOrder"    : spriteData["layerOrder"],
                "visible"       : spriteData["visible"],
                "position"      : [spriteData["x"], spriteData["y"]],
                "size"          : spriteData["size"],
                "direction"     : spriteData["direction"],
                "draggable"     : spriteData["draggable"],
                "rotationStyle" : spriteData["rotationStyle"],
            }
        newSpriteDatas.append(newSpriteData)
    stageData = projectData["targets"][0]
    newMonitorDatas = translateMonitors(
        data=projectData["monitors"],
    )
    newData = {
        "sprites"             : newSpriteDatas,
        "globalVariables"     : globalVariableDatas,
        "globalLists"         : globalListDatas,
        "tempo"               : stageData["tempo"], # I moved these from the stage to the project because they influence the whole project
        "videoTransparency"   : stageData["videoTransparency"],
        "videoState"          : stageData["videoState"],
        "textToSpeechLanguage": stageData["textToSpeechLanguage"],

        "monitors"            : newMonitorDatas,
        "extensionData"       : projectData["extensionData"],
        "extensions"          : projectData["extensions"],
        "credit"              : "https://github.com/Fritzforcode/PyPenguin"
    }
    if projectData.get("extensionURLs", {}) != {}:
        newData["extensionURLs"] = projectData["extensionURLs"]
    return newData
    