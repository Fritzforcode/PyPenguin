from pypenguin.helper_functions import pp, ikv
from pypenguin.database import getOptimizedOpcode, getOptimizedOptionID

def translateMonitors(data):
    newMonitorDatas = []
    for monitorData in data:
        #pp(monitor)
        opcode = monitorData["opcode"]
        if   opcode == "data_variable":
            newOpcode = getOptimizedOpcode(opcode="special_variable_value")
        elif opcode == "data_listcontents":
            newOpcode = getOptimizedOpcode(opcode="special_list_value")
        else:
            newOpcode = getOptimizedOpcode(opcode=opcode)
        
        newOptionDatas = {}
        for i, optionID, optionData in ikv(monitorData["params"]):
            if   opcode == "data_variable":
                newOptionID = "VARIABLE"
            elif opcode == "data_listcontents":
                newOptionID = "LIST"
            else:
                newOptionID = getOptimizedOptionID(
                    opcode=opcode,
                    optionID=optionID,
                )
            newOptionDatas[newOptionID] = optionData

        newMonitorData = {
            "opcode"    : newOpcode,
            "options"   : newOptionDatas,
            "spriteName": monitorData["spriteName"],
            "value"     : monitorData["value"],
            "size"      : [monitorData["width"], monitorData["height"]],
            "position"  : [monitorData["x"], monitorData["y"]],
            "visible"   : monitorData["visible"],
        }
        if "sliderMin" in monitorData:
            newMonitorData["sliderMin"] = monitorData["sliderMin"]
        if "sliderMax" in monitorData:
            newMonitorData["sliderMax"] = monitorData["sliderMax"]
        if "isDiscrete" in monitorData:
            newMonitorData["isDiscrete"] = monitorData["isDiscrete"]
        newMonitorDatas.append(newMonitorData)

    return newMonitorDatas
