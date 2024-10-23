from helper_functions import generateRandomToken, WhatIsGoingOnError


def translateVariables(data, spriteNames):
    tokens = {k:{} for k in spriteNames+[None]}
    newData = {k:{} for k in spriteNames+[None]}
    newMonitorDatas = []
    for variableData in data:
        sprite = variableData["sprite"]
        name = variableData["name"]
        tokens[sprite][name] = generateRandomToken()


        newVariableData = [name, variableData["currentValue"]]

        monitorData = variableData["monitor"]
        if monitorData != None:
            newMonitorData = {
                "id"        : tokens[sprite][name],
                "mode"      : "default",
                "opcode"    : "data_variable",
                "params"    : {"VARIABLE": name},
                "spriteName": sprite,
                "value"     : variableData["currentValue"],
                "width"     : monitorData["size"][0],
                "height"    : monitorData["size"][1],
                "x"         : monitorData["position"][0],
                "y"         : monitorData["position"][1],
                "visible"   : monitorData["visible"],
                "sliderMin" : monitorData["sliderMin"],
                "sliderMax" : monitorData["sliderMax"],
                "isDiscrete": monitorData["onlyIntegers"],
            }
            newMonitorDatas.append(newMonitorData)

        match variableData["mode"]:
            case "cloud":
                if not name.startswith("\u2601 "): raise ValueError("Cloud variables have to start with '☁ ' eg. '☁ var'")
            case "global":
                if "\u2601" in name: raise ValueError("Non-cloud variables cannot contain '☁'")
            case "local":
                if "\u2601" in name: raise ValueError("Non-cloud variables cannot contain '☁'")
            case _: raise WhatIsGoingOnError()
            

        newData[sprite][tokens[sprite][name]] = newVariableData
    return newData, tokens, newMonitorDatas

def translateLists(data, spriteNames):
    tokens = {k:{} for k in spriteNames+[None]}
    newData = {k:{} for k in spriteNames+[None]}
    newMonitorDatas = []
    for listData in data:
        sprite = listData["sprite"]
        name = listData["name"]
        tokens[sprite][name] = generateRandomToken()


        newListData = [name, listData["currentValue"]]

        monitorData = listData["monitor"]
        if monitorData != None:
            newMonitorData = {
                "id"        : tokens[sprite][name],
                "mode"      : "list",
                "opcode"    : "data_listcontents",
                "params"    : {"LIST": name},
                "spriteName": sprite,
                "value"     : listData["currentValue"],
                "width"     : monitorData["size"][0],
                "height"    : monitorData["size"][1],
                "x"         : monitorData["position"][0],
                "y"         : monitorData["position"][1],
                "visible"   : monitorData["visible"],
            }
            newMonitorDatas.append(newMonitorData)

        newData[sprite][tokens[sprite][name]] = newListData
    return newData, tokens, newMonitorDatas
