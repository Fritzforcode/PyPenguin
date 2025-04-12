class Target:
    _grepr = True
    _grepr_fields = ["is_stage", "name", "variables", "lists", "broadcasts", "custom_vars", "blocks", "comments", "current_costume", "costumes", "sounds", "id", "volume", "layer_order"]
    @staticmethod
    def from_data(data):
        return Target(data)
    
    def __init__(self, data):
        self.is_stage = data["isStage"]
        self.name = data["name"]
        self.variables = data["variables"]
        self.lists = data["lists"]
        self.broadcasts = data["broadcasts"]
        self.custom_vars = data["customVars"]
        self.blocks = data["blocks"]
        self.comments = data["comments"]
        self.current_costume = data["currentCostume"]
        self.costumes = data["costumes"]
        self.sounds = data["sounds"]
        self.id = data["id"]
        self.volume = data["volume"]
        self.layer_order = data["layerOrder"]
        
        self.blocks = "HAHA TEMP"

class Stage(Target):
    _grepr_fields = Target._grepr_fields + ["tempo", "video_transparency", "video_state", "text_to_speech_language"]
    @staticmethod
    def from_data(data):
        return Stage(data)

    def __init__(self, data):
        super().__init__(data)
        self.tempo = data["tempo"]
        self.video_transparency = data["videoTransparency"]
        self.video_state = data["videoState"]
        self.text_to_speech_language = data["textToSpeechLanguage"]

class Sprite(Target):
    _grepr_fields = Target._grepr_fields + ["visible", "x", "y", "size", "direction", "draggable", "rotation_style"]
    @staticmethod
    def from_data(data):
        return Sprite(data)

    def __init__(self, data):
        super().__init__(data)
        self.visible = data["visible"]
        self.x = data["x"]
        self.y = data["y"]
        self.size = data["size"]
        self.direction = data["direction"]
        self.draggable = data["draggable"]
        self.rotation_style = data["rotationStyle"]

