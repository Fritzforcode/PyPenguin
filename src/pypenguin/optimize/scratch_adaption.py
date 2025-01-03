from pypenguin.helper_functions import stringToToken

def adaptProject(data):
    for i, spriteData in enumerate(data["targets"]):
        spriteData["customVars"] = []
        if i == 0:
            token = stringToToken("_stage_")
        else:
            token = stringToToken(spriteData["name"])
        spriteData["id"        ] = token
    
    data["extensionData"] = {}

    data["meta"] = {
        "semver": "3.0.0",
        "vm"    : "0.2.0",
        "agent" : "",
        "platform": {
            "name"   : "PenguinMod",
            "url"    : "https://penguinmod.com/",
            "version": "stable",
        },
    }

    return data
