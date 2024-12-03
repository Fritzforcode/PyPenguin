from .constants import validateSchema, formatError, variableSchema, listSchema

def validateVariable(path, data, isGlobal):    
    # Check variable format
    validateSchema(pathToData=path, data=data, schema=variableSchema)
    if isGlobal and "isCloudVariable" not in data:
        raise formatError(path=path, message="Global variables must have the 'isCloudVariable' attribute.")
    #monitor = data["monitor"]
    #if monitor != None:
    #    if not monitor["sliderMin"] <= monitor["sliderMax"]:
    #        raise formatError(path=path, message="'sliderMin' must be below 'sliderMax'.")
    #    if monitor["onlyIntegers"]:
    #        if not isinstance(monitor["sliderMin"], int):
    #            raise formatError(path=path+["monitor"]+["sliderMin"], message="Must be an integer because 'onlyIntegers' is true.")
    #        if not isinstance(monitor["sliderMax"], int):
    #            raise formatError(path=path+["monitor"]+["sliderMax"], message="Must be an integer because 'onlyIntegers' is true.")
        
def validateList(path, data):
    # Check list format
    validateSchema(pathToData=path, data=data, schema=listSchema)