from pypenguin.helper_functions import pp
from pypenguin.validate.constants import validateSchema, formatError, projectSchema
from pypenguin.validate.variables_lists import validateVariable, validateList
from pypenguin.validate.sprites import validateSprite
from pypenguin.validate.monitors import validateMonitor
from pypenguin.database import defaultCostume
import copy

def validateProject(projectData):
    projectDataCopy = copy.deepcopy(projectData)
    # Check project format
    validateSchema(pathToData=[], data=projectDataCopy, schema=projectSchema)
    
    # Check variable formats
    errorMessage = "Variable names mustn't be the same. Please check 'globalVariables' and 'localVariables' of the same sprite."
    globalVariableNames = []
    for j, variable in enumerate(projectDataCopy["globalVariables"]):
        validateVariable(path=["globalVariables"]+[j], data=variable, isGlobal=True)
        variableName = variable["name"]
        if variableName in globalVariableNames: # if var name alredy exists globally
            raise formatError(path=["globalVariables"]+[j]+["name"], message=errorMessage)
    
    localVariableNames = [[] for i in range(  len( projectDataCopy["sprites"][1:] )  )]
    for i, sprite in enumerate(projectDataCopy["sprites"][1:]):
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
    for j, list_ in enumerate(projectDataCopy["globalLists"]):
        validateList(path=["globalLists"]+[j], data=list_)
        listName = list_["name"]
        if listName in globalListNames: # if list name alredy exists globally
            raise formatError(path=["globalLists"]+[j]+["name"], message=errorMessage)
    
    localListNames = [[] for i in range(  len( projectDataCopy["sprites"][1:] )  )]
    for i, sprite in enumerate(projectDataCopy["sprites"][1:]):
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
    spriteNames    = []
    localVariables = {}
    localLists     = {}
    otherSprites   = []
    for i, sprite in enumerate(projectDataCopy["sprites"]):
        if i == 0: spriteName = ["stage", "stage"]
        else:      spriteName = ["sprite", sprite["name"]]
        if spriteName in spriteNames: # If there is the same sprite name twice
            raise formatError(path=["sprites"]+[i]+["name"], message="Sprite names mustn't be the same.")
        spriteNames.append(spriteName)
        

        if i == 0:
            if "costumes" not in sprite:
                raise formatError(path=["sprites"]+[i], message="Must have the 'costumes' attribute.")
            backdrops = [["costume", costume["name"]] for costume in sprite["costumes"]]
            if sprite["costumes"] == []:
                backdrops.insert(0, ["costume", defaultCostume["name"]])
            
        else:
            otherSprites.append(spriteName)
            localVariables[tuple(spriteName)] = [["variable", item["name"]] for item in sprite["localVariables"]]
            localLists    [tuple(spriteName)] = [["list"    , item["name"]] for item in sprite["localLists"    ]]
    
    contexts = {}
    for i, sprite in enumerate(projectDataCopy["sprites"]):
        if i == 0:
            scopeVariables    = [["variable", item["name"]] for item in projectDataCopy["globalVariables"]]
            scopeLists        = [["list"    , item["name"]] for item in projectDataCopy["globalLists"    ]]
            nameKey           = None
        else:
            scopeVariables    = [["variable", item["name"]] for item in sprite["localVariables"] + projectDataCopy["globalVariables"]]
            scopeLists        = [["list"    , item["name"]] for item in sprite["localLists"    ] + projectDataCopy["globalLists"    ]]
            nameKey           = sprite["name"]

        context = {
            "scopeVariables" : scopeVariables, 
            "scopeLists"     : scopeLists, 
            "globalVariables": [["variable", item["name"]] for item in projectDataCopy["globalVariables"]],
            "localVariables" : localVariables,
            "localLists"     : localLists,
            "otherSprites": [
                target for target in otherSprites if target[1] != sprite["name"]
            ],
            "backdrops": backdrops,
        }
        validateSprite(path=["sprites"]+[i], data=sprite, context=context)
        contexts[nameKey] = context

    for i, monitorData in enumerate(projectDataCopy["monitors"]):
        validateMonitor(
            path=["monitors"]+[i], 
            data=monitorData, 
            contexts=contexts
        )
