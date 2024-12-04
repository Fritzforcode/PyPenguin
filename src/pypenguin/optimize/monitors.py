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
            "position"  : [monitorData["x"], monitorData["y"]],
            "visible"   : monitorData["visible"],
        }
        if opcode == "data_variable":
            newMonitorData["sliderMin"] = monitorData["sliderMin"]
            newMonitorData["sliderMax"] = monitorData["sliderMax"]
            newMonitorData["onlyIntegers"] = monitorData["isDiscrete"]
        elif opcode == "data_listcontents":
            newMonitorData["size"] = [monitorData["width"], monitorData["height"]]
        newMonitorDatas.append(newMonitorData)

    return newMonitorDatas
