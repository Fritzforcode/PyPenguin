from pypenguin.database import defaultCostume
from pypenguin.validate.constants import validateSchema, formatError, stageSchema, spriteSchema
from pypenguin.validate.costumes_sounds import validateCostume, validateSound
from pypenguin.validate.blocks_scripts import validateScript
from pypenguin.validate.comments import validateComment

def validateSprite(path, data, context):
    i = path[-1]
    if i == 0: # If it should be the stage
        # Check stage format
        validateSchema(pathToData=path, data=data, schema=stageSchema)
        if data["name"] != "Stage": 
            raise formatError(path+["name"], "'name' of the stage (the first sprite) must always be 'Stage'.")
    else: # If it should be a sprite
        # Check sprite format
        validateSchema(pathToData=path, data=data, schema=spriteSchema)
        
        if data["name"] in ["_myself_", "_stage_"]:
            raise formatError(path+["name"], f"'{data['name']}' isn't a valid sprite name. Please pick another name.")
        if data["layerOrder"] < 1:
            raise formatError(path+["layerOrder"], "'layerOrder' of a sprite must be at least 1.")
        
    # Check script formats
    for j, script in enumerate(data["scripts"]):
        validateScript(path=path+["scripts"]+[j], data=script, context=context)
    
    # Check comment formats
    for j, comment in enumerate(data["comments"]):
        validateComment(path=path+["comments"]+[j], data=comment)

    # Check costume formats
    if len(data["costumes"]) < 1:
        #raise formatError(path=path+["costumes"], message="Each sprite must have at least one costume.")
        data["costumes"].append(defaultCostume)
    costumeNames = []
    for j, costume in enumerate(data["costumes"]):
        validateCostume(path=path+["costumes"]+[j], data=costume, isStage=i==0)
        if costume["name"] in costumeNames: # If a costume with the same name alredy exists
            raise formatError(path=path+["costumes"]+[j]+["name"], message= "Costume names mustn't be the same.")
        costumeNames.append(costume["name"])
    
    # Check sound formats
    soundNames = []
    for j, sound in enumerate(data["sounds"]):
        validateSound(path=path+["sounds"]+[j], data=sound)
        if sound["name"] in soundNames: # If a sound with the same name alredy exists
            raise formatError(path=path+["sounds"]+[j]+["name"], message= "Sound names mustn't be the same.")
        soundNames.append(sound["name"])
    
    
    # Make sure that currentCostume refers to an existing costume
    if data["currentCostume"] >= len(data["costumes"]):
        raise formatError(path=path+["currentCostume"], message=f"Is out of range. There are only {len(data['costumes'])} costumes in this sprite, so 'currentCostume' could be at most {len(data['costumes']) - 1}.")