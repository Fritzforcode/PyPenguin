def translateComment(data):
    return {
        "position" : [data["x"], data["y"]],
        "size"     : [data["width"], data["height"]],
        "minimized": data["minimized"],
        "text"     : data["text"],
    }
