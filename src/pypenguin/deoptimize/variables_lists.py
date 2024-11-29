from pypenguin.helper_functions import WhatIsGoingOnError, pp, stringToToken


def translateVariables(data, spriteNames):
    newData = {k:{} for k in spriteNames+[None]}
    newMonitorDatas = []
    for spriteData in data["sprites"]:
        if spriteData["isStage"]:
            spriteName = None
            localVariableDatas = data["globalVariables"]
        else:
            spriteName = spriteData["name"]
            localVariableDatas = spriteData["localVariables"]
        for variableData in localVariableDatas:
            newVariableData, newMonitorData = translateVariable(data=variableData, spriteName=spriteName)
            token = stringToToken(variableData["name"], spriteName=spriteName)
            newData[spriteName][token] = newVariableData
            if newMonitorData != None:
                newMonitorDatas.append(newMonitorData)
    return newData, newMonitorDatas

def translateVariable(data, spriteName):
    name = data["name"]
    newData = [name, data["currentValue"]]

    monitorData = data["monitor"]
    if monitorData == None:
        newMonitorData = None
    else:
        newMonitorData = {
            "id"        : stringToToken(name, spriteName=spriteName),
            "mode"      : "default",
            "opcode"    : "data_variable",
            "params"    : {"VARIABLE": name},
            "spriteName": spriteName,
            "value"     : data["currentValue"],
            "width"     : monitorData["size"][0],
            "height"    : monitorData["size"][1],
            "x"         : monitorData["position"][0],
            "y"         : monitorData["position"][1],
            "visible"   : monitorData["visible"],
            "sliderMin" : monitorData["sliderMin"],
            "sliderMax" : monitorData["sliderMax"],
            "isDiscrete": monitorData["onlyIntegers"],
        }
    if spriteName == None: # stage
        if data["isCloudVariable"]: # cloud var
            if not name.startswith("\u2601 "):
                raise ValueError("Cloud variables have to start with '☁ ' eg. '☁ var' (☁: unicode 2601)")
            newData.append(True)
        else: # global var
            if "\u2601" in name:
                raise ValueError("Non-cloud variables cannot contain '☁'(unicode 2601)")
    else: # local var
        if "\u2601" in name:
            raise ValueError("Non-cloud variables cannot contain '☁'(unicode 2601)")
    return newData, newMonitorData

def translateLists(data, spriteNames):
    newData = {k:{} for k in spriteNames+[None]}
    newMonitorDatas = []
    for spriteData in data["sprites"]:
        if spriteData["isStage"]:
            spriteName = None
            localListDatas = data["globalLists"]
        else:
            spriteName = spriteData["name"]
            localListDatas = spriteData["localLists"]
        for listData in localListDatas:
            newListData, newMonitorData = translateList(data=listData, spriteName=spriteName)
            token = stringToToken(listData["name"], spriteName=spriteName)
            newData[spriteName][token] = newListData
            if newMonitorData != None:
                newMonitorDatas.append(newMonitorData)
    return newData, newMonitorDatas

def translateList(data, spriteName):
    name = data["name"]
    newData = [name, data["currentValue"]]

    monitorData = data["monitor"]
    if monitorData == None:
        newMonitorData = None
    else:
        newMonitorData = {
            "id"        : stringToToken(name, spriteName=spriteName),
            "mode"      : "list",
            "opcode"    : "data_listcontents",
            "params"    : {"LIST": name},
            "spriteName": spriteName,
            "value"     : data["currentValue"],
            "width"     : monitorData["size"][0],
            "height"    : monitorData["size"][1],
            "x"         : monitorData["position"][0],
            "y"         : monitorData["position"][1],
            "visible"   : monitorData["visible"],
        }
    return newData, newMonitorData

