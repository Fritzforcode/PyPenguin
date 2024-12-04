from pypenguin.validate.constants import validateSchema, monitorSchema, formatError
from pypenguin.validate.blocks_scripts import validateOptions
from pypenguin.helper_functions import pp
from pypenguin.database import getDeoptimizedOpcode

def validateMonitor(path, data, contexts):
    validateSchema(pathToData=path, data=data, schema=monitorSchema)

    opcode      = getDeoptimizedOpcode(opcode=data["opcode"])
    spriteNames = list(contexts.keys())
    if data["spriteName"] not in spriteNames:
        raise formatError(path=path+["spriteName"], message=f"Must be the name of an existing sprite. Must be one of these: {spriteNames}.")
    
    validateOptions(
        path=path+["options"],
        data=data["options"],
        opcode=data["opcode"],
        context=contexts[data["spriteName"]],
        inputDatas=None,
    )

    if   opcode == "special_variable_value":
        required = ["sliderMin", "sliderMax", "onlyIntegers"]
    elif opcode == "special_list_value":
        required = ["size"]
    else:
        required = []
    
    for attribute in required:
        if attribute not in data:
            raise formatError(path=path, message=f"Must have the '{attribute}' attribute.")

    if   opcode == "special_variable_value":
        if not (data["sliderMin"] <= data["sliderMax"]):
            raise formatError(path=path, message="'sliderMin' must be below 'sliderMax'.")
        if data["onlyIntegers"]:
            if not isinstance(data["sliderMin"], int):
                raise formatError(path=path+["monitor"]+["sliderMin"], message="Must be an integer because 'onlyIntegers' is true.")
            if not isinstance(data["sliderMax"], int):
                raise formatError(path=path+["monitor"]+["sliderMax"], message="Must be an integer because 'onlyIntegers' is true.")