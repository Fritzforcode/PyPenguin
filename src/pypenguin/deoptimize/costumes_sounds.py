from pypenguin.database import defaultCostumeDeoptimized

def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        newCostumeData = {
            "name"            : costumeData["name"],
            "bitmapResolution": None,
            "assetId"         : costumeData["fileStem"],
            "dataFormat"      : costumeData["dataFormat"],
            "md5ext"          : costumeData["fileStem"] + "." + costumeData["dataFormat"],
            "rotationCenterX" : costumeData["rotationCenter"][0],
            "rotationCenterY" : costumeData["rotationCenter"][1],
        }
        if "bitmapResolution" in costumeData:
            newCostumeData["bitmapResolution"] = costumeData["bitmapResolution"]
        else:
            del newCostumeData["bitmapResolution"]
        newCostumeDatas.append(newCostumeData)
    if newCostumeDatas == []: # When there are no costumes
        defaultCostumeModified = defaultCostumeDeoptimized.copy() | {"isDefault": True}
        newCostumeDatas.append(defaultCostumeModified)
    return newCostumeDatas

def translateSounds(data):
    newSoundDatas = []
    for soundData in data:
        newSoundData = {
            "name"       : soundData["name"],
            "assetId"    : soundData["fileStem"],
            "dataFormat" : soundData["dataFormat"],
            "rate"       : soundData["rate"],        # playback speed in Hz
            "sampleCount": soundData["sampleCount"], # = "rate" * duration in secs
            "md5ext"     : soundData["fileStem"] + "." + soundData["dataFormat"],
        }
        newSoundDatas.append(newSoundData)
    return newSoundDatas
