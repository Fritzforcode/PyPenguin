exec("import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))")

from helper_functions import readJSONFile, writeJSONFile

from optimize.costumes_sounds import translateCostumes, translateSounds
from optimize.variables_lists import translateVariables, translateLists
from optimize.blocks_scripts import translateScript, generateBlockChildrenPs
from optimize.comments import translateComment

opcodeDatabase = readJSONFile("assets/opcode_database.jsonc")


def optimizeProject(projectData):
    newSpriteDatas = []
    for i, spriteData in enumerate(projectData["targets"]):
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
        translatedVariableDatas = translateVariables(
            data=spriteData, 
            monitorDatas=projectData["monitors"]
        )
        translatedListDatas = translateLists(
            data=spriteData,
            monitorDatas=projectData["monitors"],
        )
        #pp(spriteData)
        #pp(translatedVariableDatas)
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
    newData = {
        "sprites"             : newSpriteDatas,
        "globalVariables"     : globalVariableDatas,
        "globalLists"         : globalListDatas,
        "tempo"               : stageData["tempo"], # I moved these from the stage to the project because they influence the whole project
        "videoTransparency"   : stageData["videoTransparency"],
        "videoState"          : stageData["videoState"],
        "textToSpeechLanguage": stageData["textToSpeechLanguage"],

        "extensionData"       : projectData["extensionData"],
        "extensions"          : projectData["extensions"],
        "meta"                : projectData["meta"],
    }
    return newData
