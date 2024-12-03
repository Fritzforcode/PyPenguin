from pypenguin.validate.constants import validateSchema, monitorSchema

def validateMonitor(path, data):
    validateSchema(pathToData=path, data=data, schema=monitorSchema)
    

