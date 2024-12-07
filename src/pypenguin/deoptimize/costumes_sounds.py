from pypenguin.database import defaultCostumeDeoptimized
from pypenguin.helper_functions import pp

def translateCostumes(data):
    newCostumeDatas = []
    for costumeData in data:
        newCostumeData = {
            "name"            : costumeData["name"],
            "assetId"         : None, # is replaced later
            "dataFormat"      : costumeData["extension"],
            "md5ext"          : None, # is replaced later
            "rotationCenterX" : costumeData["rotationCenter"][0],
            "rotationCenterY" : costumeData["rotationCenter"][1],
        }
        if "bitmapResolution" in costumeData:
            newCostumeData["bitmapResolution"] = costumeData["bitmapResolution"]
        newCostumeDatas.append(newCostumeData)
    if newCostumeDatas == []: # When there are no costumes
        defaultCostumeModified = defaultCostumeDeoptimized.copy() | {"isDefault": True}
        newCostumeDatas.append(defaultCostumeModified)
    return newCostumeDatas

def finalizeCostume(data, md5, md5ext):
    # Integrate md5 hash, keep all other attributes
    newData = {
        "name"            : data["name"],
        "assetId"         : md5,
        "dataFormat"      : data["dataFormat"],
        "md5ext"          : md5ext,
        "rotationCenterX" : data["rotationCenterX"],
        "rotationCenterY" : data["rotationCenterY"],
    }
    if "bitmapResolution" in data:
        newData["bitmapResolution"] = data["bitmapResolution"]
    return newData

def translateSounds(data):
    newSoundDatas = []
    for soundData in data:
        newSoundData = {
            "name"       : soundData["name"],
            "assetId"    : None, # is replaced later
            "dataFormat" : soundData["extension"],
            "rate"       : soundData["rate"],        # playback speed in Hz
            "sampleCount": soundData["sampleCount"], # = "rate" * SECONDS in secs
            "md5ext"     : None, # is replaced later
        }
        newSoundDatas.append(newSoundData)
    return newSoundDatas

def finalizeSound(data, md5, md5ext):
    newData = {
        "name"       : data["name"],
        "assetId"    : md5,
        "dataFormat" : data["dataFormat"],
        "rate"       : data["rate"],
        "sampleCount": data["sampleCount"],
        "md5ext"     : md5ext,
    }
    return newData
