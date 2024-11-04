from .constants import validateSchema, formatError, projectSchema
from .variables_lists import validateVariable, validateList
from .sprites import validateSprite

def validateProject(projectData):
    # Check project format
    validateSchema(pathToData=[], data=projectData, schema=projectSchema)
    
    # Check variable formats
    errorMessage = "Variable names mustn't be the same. Please check 'globalVariables' and 'localVariables' of the same sprite."
    globalVariableNames = []
    for j, variable in enumerate(projectData["globalVariables"]):
        validateVariable(path=["globalVariables"]+[j], data=variable, isGlobal=True)
        variableName = variable["name"]
        if variableName in globalVariableNames: # if var name alredy exists globally
            raise formatError(path=["globalVariables"]+[j]+["name"], message=errorMessage)
    
    localVariableNames = [[] for i in range(  len( projectData["sprites"][1:] )  )]
    for i, sprite in enumerate(projectData["sprites"][1:]):
        if "localVariables" not in sprite:
            raise formatError(path=["sprites"]+[i], message="Each sprite (but not the stage) must have the 'localVariables' attribute.")
        if not isinstance(sprite["localVariables"], list):
            raise formatError(path=["sprites"]+[i]+["localVariables"], message="Must be an array.")
        
        for j, variable in enumerate(sprite["localVariables"]):
            validateVariable(path=["sprites"]+[i]+["localVariables"]+[j], data=variable, isGlobal=False)
            variableName = variable["name"]
            if variableName in globalVariableNames or variableName in localVariableNames[i]: # if var name alredy exists globally or in the same sprite
                raise formatError(path=["sprites"]+[i]+["localVariables"]+[j]+["name"], message=errorMessage)
    
    
    errorMessage = "List names mustn't be the same. Please check 'globalLists' and 'localLists' of the same sprite."
    globalListNames = []
    for j, list_ in enumerate(projectData["globalLists"]):
        validateList(path=["globalLists"]+[j], data=list_)
        listName = list_["name"]
        if listName in globalListNames: # if list name alredy exists globally
            raise formatError(path=["globalLists"]+[j]+["name"], message=errorMessage)
    
    localListNames = [[] for i in range(  len( projectData["sprites"][1:] )  )]
    for i, sprite in enumerate(projectData["sprites"][1:]):
        if "localLists" not in sprite:
            raise formatError(path=["sprites"]+[i], message="Each sprite (but not the stage) must have the 'localLists' attribute.")
        if not isinstance(sprite["localLists"], list):
            raise formatError(path=["sprites"]+[i]+["localLists"], message="Must be an array.")
        
        for j, list_ in enumerate(sprite["localLists"]):
            validateList(path=["sprites"]+[i]+["localLists"]+[j], data=list_)
            listName = list_["name"]
            if listName in globalListNames or listName in localListNames[i]: # if list name alredy exists globally or in the same sprite
                raise formatError(path=["sprites"]+[i]+["localLists"]+[j]+["name"], message=errorMessage)
    

    # Check sprite formats
    spriteNames = []
    for i, sprite in enumerate(projectData["sprites"]):
        if i == 0:
            scopeVariables = projectData["globalVariables"]
            scopeLists     = projectData["globalLists"]
        else:
            scopeVariables = sprite["localVariables"] + projectData["globalVariables"]
            scopeLists     = sprite["localLists"]     + projectData["globalLists"]
        
        context = {"scopeVariables": scopeVariables, "scopeLists": scopeLists}
        validateSprite(path=["sprites"]+[i], data=sprite, context=context)
        spriteName = None if i == 0 else sprite["name"] # None for the stage
        if spriteName in spriteNames: # If there is the same sprite name twice
            raise formatError(path=["sprites"]+[i]+["name"], message="Sprite names mustn't be the same.")
        spriteNames.append(spriteName)

