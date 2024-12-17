from pypenguin.helper_functions import ikv


def translateVariables(data):
    newData = []
    for i,variableID,variableData in ikv(data["variables"]):
        name = variableData[0]
        currentValue = variableData[1]
        if data["isStage"]:
            if len(variableData) == 3 and variableData[2] == True:
                mode = "cloud"
            else:
                mode = "global"
            sprite = None
        else:
            mode = "local"
            sprite = data["name"]
        if data["customVars"] != []:
            raise Exception("Wow! I have been trying to find out what 'customVars' is used for. Can you explain how you did that? Please contact me on GitHub.")
        
        #monitorIDs = [i["id"] for i in monitorDatas]
        ## if there is no monitor for that variable
        #if variableID not in monitorIDs:
        #    newMonitorData = None
        #else:
        #    monitorData = monitorDatas[monitorIDs.index(variableID)]
        #    newMonitorData = {
        #        "visible"     : monitorData["visible"],
        #        "size"        : [monitorData["width"], monitorData["height"]],
        #        "position"    : [monitorData["x"], monitorData["y"]],
        #        "sliderMin"   : monitorData["sliderMin"],
        #        "sliderMax"   : monitorData["sliderMax"],
        #        "onlyIntegers": monitorData["isDiscrete"],
        #    }
        
        newVariableData = {
            "name"        : name,
            "currentValue": currentValue,
        }
        if mode == "global":
            newVariableData["isCloudVariable"] = False
        elif mode == "cloud":
            newVariableData["isCloudVariable"] = True
        elif mode == "local":
            pass
        newData.append(newVariableData)
    return newData
    
def translateLists(data):
    newData = []
    for i,listID,listData in ikv(data["lists"]):
        name = listData[0]
        currentValue = listData[1]
        
        #monitorIDs = [i["id"] for i in monitorDatas]
        ## if there is no monitor for that list
        #if listID not in monitorIDs:
        #    newMonitorData = None
        #else:
        #    monitorData = monitorDatas[monitorIDs.index(listID)]
        #    newMonitorData = {
        #        "visible"     : monitorData["visible"],
        #        "size"        : [monitorData["width"], monitorData["height"]],
        #        "position"    : [monitorData["x"], monitorData["y"]],
        #    }
        
        newListData = {
            "name"        : name,
            "currentValue": currentValue,
        }
        newData.append(newListData)
    return newData
