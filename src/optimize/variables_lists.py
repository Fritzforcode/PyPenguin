from helper_functions import ikv, WhatIsGoingOnError


def translateVariables(data, monitorDatas):
    newData = []
    for spriteData in data:
        for i,variableID,variableData in ikv(spriteData["variables"]):
            name = variableData[0]
            currentValue = variableData[1]
            if spriteData["isStage"]:
                if len(variableData) == 3 and variableData[2] == True:
                    mode = "cloud"
                else:
                    mode = "global"
                sprite = None
            else:
                mode = "local"
                sprite = spriteData["name"]
            if spriteData["customVars"] != []:
                raise WhatIsGoingOnError("Wow! I have been trying to find out what 'customVars' is used for. Can you explain how you did that? Please contact me on GitHub.")
            
            monitorIDs = [i["id"] for i in monitorDatas]
            # if there is no monitor for that variable
            if variableID not in monitorIDs:
                newMonitorData = None
            else:
                monitorData = monitorDatas[monitorIDs.index(variableID)]
                newMonitorData = {
                    "visible"     : monitorData["visible"],
                    "size"        : [monitorData["width"], monitorData["height"]],
                    "position"    : [monitorData["x"], monitorData["y"]],
                    "sliderMin"   : monitorData["sliderMin"],
                    "sliderMax"   : monitorData["sliderMax"],
                    "onlyIntegers": monitorData["isDiscrete"],
                }
            
            newVariableData = {
                "name"        : name,
                "currentValue": currentValue,
                "mode"        : mode,
                "sprite"      : sprite,
                "monitor"     : newMonitorData,
            }
            newData.append(newVariableData)
    return newData

def translateLists(data, monitorDatas):
    newData = []
    for spriteData in data:
        for i,listID,listData in ikv(spriteData["lists"]):
            name = listData[0]
            currentValue = listData[1]
            if spriteData["isStage"]:
                mode = "global"
                sprite = None
            else:
                mode = "local"
                sprite = spriteData["name"]
            
            monitorIDs = [i["id"] for i in monitorDatas]
            # if there is no monitor for that variable
            if listID not in monitorIDs:
                newMonitorData = None
            else:
                monitorData = monitorDatas[monitorIDs.index(listID)]
                newMonitorData = {
                    "visible"     : monitorData["visible"],
                    "size"        : [monitorData["width"], monitorData["height"]],
                    "position"    : [monitorData["x"], monitorData["y"]],
                }
            
            newListData = {
                "name"        : name,
                "currentValue": currentValue,
                "mode"        : mode,
                "sprite"      : sprite,
                "monitor"     : newMonitorData,
            }
            newData.append(newListData)
    return newData
