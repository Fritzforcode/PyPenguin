from gimport import gimport
utility = gimport("utility/")
from utility import gprint


class Monitor:
    _grepr = True
    _grepr_fields = []
    @staticmethod
    def from_data(data):
        return Monitor(data)
    
    def __init__(self, data):
        gprint(data)
        """self.is_stage = data["isStage"]
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
        self.layer_order = data["layerOrder"]"""
        

