from validate.constants import formatError, validateSchema, costumeSchema, soundSchema

def validateCostume(path, data, isStage):
    # Check costume format
    validateSchema(pathToData=path, data=data, schema=costumeSchema)
    if "bitmapResolution" not in data:
        ###if not(isStage and data["dataFormat"] == "svg"):
        ###    raise formatError(path=path, message="Unless the costume is a backdrop and a .svg, the 'bitmapResolution' attribute is required.")
        raise formatError(path=path, message="'bitmapResolution' is a required attribute.")
    
def validateSound(path, data):
    # Check sound format
    validateSchema(pathToData=path, data=data, schema=soundSchema)

