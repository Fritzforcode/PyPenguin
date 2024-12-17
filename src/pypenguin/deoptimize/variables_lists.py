from pypenguin.helper_functions import stringToToken


def translateVariables(data, spriteNames):
    newData = {k:{} for k in spriteNames+[None]}
    for spriteData in data["sprites"]:
        if spriteData["isStage"]:
            spriteName = None
            localVariableDatas = data["globalVariables"]
        else:
            spriteName = spriteData["name"]
            localVariableDatas = spriteData["localVariables"]
        for variableData in localVariableDatas:
            newVariableData = translateVariable(data=variableData, spriteName=spriteName)
            token = stringToToken(variableData["name"], spriteName=spriteName)
            newData[spriteName][token] = newVariableData
    return newData

def translateVariable(data, spriteName):
    name = data["name"]
    newData = [name, data["currentValue"]]

    if spriteName == None: # stage
        if data["isCloudVariable"]: # cloud var
            pass#if not name.startswith("\u2601 "):
            #    raise ValueError("Cloud variables have to start with '☁ ' eg. '☁ var' (☁: unicode 2601)")
            newData.append(True)
        else: # global var
            pass#if "\u2601" in name:
            #    raise ValueError("Non-cloud variables cannot contain '☁'(unicode 2601)")
    else: # local var
        pass#if "\u2601" in name:
        #    raise ValueError("Non-cloud variables cannot contain '☁'(unicode 2601)")
    return newData

def translateLists(data, spriteNames):
    newData = {k:{} for k in spriteNames+[None]}
    for spriteData in data["sprites"]:
        if spriteData["isStage"]:
            spriteName = None
            localListDatas = data["globalLists"]
        else:
            spriteName = spriteData["name"]
            localListDatas = spriteData["localLists"]
        for listData in localListDatas:
            newListData = translateList(data=listData, spriteName=spriteName)
            token = stringToToken(listData["name"], spriteName=spriteName)
            newData[spriteName][token] = newListData
    return newData

def translateList(data, spriteName):
    name = data["name"]
    newData = [name, data["currentValue"]]
    
    return newData

