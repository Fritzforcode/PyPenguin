def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        newCostumeData = {
            "name"            : costumeData["name"],
            "extension"       : costumeData["dataFormat"],
            "bitmapResolution": None,
            "rotationCenter"  : [costumeData["rotationCenterX"], costumeData["rotationCenterY"]],
        }
        if "bitmapResolution" in costumeData:
            newCostumeData["bitmapResolution"] = costumeData["bitmapResolution"]
        else:
            newCostumeData["bitmapResolution"] = 1
        newCostumeDatas.append(newCostumeData)
    return newCostumeDatas

def translateSounds(data):
    newSoundDatas = []
    for soundData in data:
        newSoundData = {
            "name"       : soundData["name"],
            "extension"  : soundData["dataFormat"],
            "rate"       : soundData["rate"],        # playback speed in Hz
            "sampleCount": soundData["sampleCount"], # = "rate" * SECONDS in secs
        }
        newSoundDatas.append(newSoundData)
    return newSoundDatas
