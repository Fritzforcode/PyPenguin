def validateSprite(path, data, context):
    from validate.constants import validateSchema, formatError, stageSchema, spriteSchema
    from validate.costumes_sounds import validateCostume, validateSound
    from validate.blocks_scripts import validateScript

    i = path[-1]
    if i == 0: # If it should be the stage
        # Check stage format
        validateSchema(pathToData=path, data=data, schema=stageSchema)
        if data["name"] != "Stage": 
            raise formatError(path, "'name' of the stage (the first sprite) must always be 'Stage'.")
    else: # If it should be a sprite
        # Check sprite format
        validateSchema(pathToData=path, data=data, schema=spriteSchema)
        
        if data["layerOrder"] < 1:
            raise formatError(path, "'layerOrder' of a sprite must be at least 1.")
        
    # Check script formats
    for j, script in enumerate(data["scripts"]):
        validateScript(path=path+["scripts"]+[j], data=script, context=context)
    
    # Check costume formats
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