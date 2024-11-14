from pypenguin.helper_functions import generateRandomToken, WhatIsGoingOnError, pp


def translateVariables(data, spriteNames):
    tokens = {k:{} for k in spriteNames+[None]}
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
            token, newVariableData, newMonitorData = translateVariable(data=variableData, spriteName=spriteName)
            tokens[spriteName][variableData["name"]] = token
            newData[spriteName][token] = newVariableData
            if newMonitorData != None:
                newMonitorDatas.append(newMonitorData)
    return newData, tokens, newMonitorDatas

def translateVariable(data, spriteName):
    token = generateRandomToken()
    name = data["name"]
    newData = [name, data["currentValue"]]

    monitorData = data["monitor"]
    if monitorData == None:
        newMonitorData = None
    else:
        newMonitorData = {
            "id"        : token,
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
    return token, newData, newMonitorData

def translateLists(data, spriteNames):
    tokens = {k:{} for k in spriteNames+[None]}
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
            token, newListData, newMonitorData = translateList(data=listData, spriteName=spriteName)
            tokens[spriteName][listData["name"]] = token
            newData[spriteName][token] = newListData
            if newMonitorData != None:
                newMonitorDatas.append(newMonitorData)
    return newData, tokens, newMonitorDatas

def translateList(data, spriteName):
    token = generateRandomToken()
    name = data["name"]
    newData = [name, data["currentValue"]]

    monitorData = data["monitor"]
    if monitorData == None:
        newMonitorData = None
    else:
        newMonitorData = {
            "id"        : token,
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
    return token, newData, newMonitorData

