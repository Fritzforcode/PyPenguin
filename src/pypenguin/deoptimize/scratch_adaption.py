def adaptProject(data):
    for i, targetData in enumerate(data["targets"]):
        del targetData["customVars"]
        del targetData["id"]
    
    del data["extensionData"]
    if "extensionURLs" in data:
        del data["extensionURLs"]

    data["meta"] = {
        "semver": "3.0.0",
        "vm": "5.0.40",
        "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    return data
