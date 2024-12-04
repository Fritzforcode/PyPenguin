from pypenguin.validate.constants import validateSchema, monitorSchema
from pypenguin.validate.blocks_scripts import validateOptions
from pypenguin.helper_functions import ikv
from pypenguin.database import getOptionTypes, getDeoptimizedOpcode

def validateMonitor(path, data, context):
    validateSchema(pathToData=path, data=data, schema=monitorSchema)
    
    validateOptions(
        path=path+["options"],
        data=data["options"],
        opcode=data["opcode"],
        context=context,
        inputDatas=None,
    )    
