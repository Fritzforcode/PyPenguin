from pypenguin.database import getOptimizedOpcode, getOptimizedOptionID, optimizeOptionValue, getOptionType

def translateMonitors(data, spriteNames):
    newMonitorDatas = []
    for monitorData in data:
        opcode = monitorData["opcode"]
        if   opcode == "data_variable":
            newOpcode = getOptimizedOpcode(opcode="special_variable_value")
        elif opcode == "data_listcontents":
            newOpcode = getOptimizedOpcode(opcode="special_list_value")
        else:
            newOpcode = getOptimizedOpcode(opcode=opcode)
        
        newOptionDatas = {}
        for optionID, optionData in monitorData["params"].items():
            if   opcode == "data_variable":
                newOptionID = "VARIABLE"
                optionType  = "variable"
            elif opcode == "data_listcontents":
                newOptionID = "LIST"
                optionType  = "list"
            else:
                newOptionID = getOptimizedOptionID(
                    opcode=opcode,
                    optionID=optionID,
                )
                optionType = getOptionType(
                    opcode=opcode, 
                    optionID=optionID
                )
            newOptionData = optimizeOptionValue(
                optionValue=optionData,
                optionType=optionType,
            )
            newOptionDatas[newOptionID] = newOptionData

        newMonitorData = {
            "opcode"    : newOpcode,
            "options"   : newOptionDatas,
            "spriteName": monitorData["spriteName"],
            "position"  : [monitorData["x"], monitorData["y"]],
            "visible"   : monitorData["visible"],
        }
        if opcode == "data_variable":
            newMonitorData["sliderMin"] = monitorData["sliderMin"]
            newMonitorData["sliderMax"] = monitorData["sliderMax"]
            newMonitorData["onlyIntegers"] = monitorData["isDiscrete"]
        elif opcode == "data_listcontents":
            newMonitorData["size"] = [monitorData["width"], monitorData["height"]]
        if (newMonitorData["spriteName"] not in spriteNames) and not(newMonitorData["visible"]):
            continue
        newMonitorDatas.append(newMonitorData)

    return newMonitorDatas
