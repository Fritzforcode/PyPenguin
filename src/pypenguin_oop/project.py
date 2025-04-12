import json

from gimport import gimport
utility = gimport("utility/")
from utility import gprint, read_file_of_zip
target = gimport("target.py")
monitor = gimport("monitor.py")

class Project:
    _grepr = True
    _grepr_fields = ["targets", "monitors", "extensionData", "extensions", "meta"]
    @staticmethod
    def from_pmp_file(file_path):
        return Project(file_path)
    
    def __init__(self, file_path):    
        project_data = json.loads(read_file_of_zip(file_path, "project.json"))
        
        self.targets = []
        for i, target_data in enumerate(project_data["targets"]):
            self.targets.append(
              target.Stage.from_data(target_data) if i==0 else target.Sprite.from_data(target_data)
            )
        
        self.monitors = []
        for monitor_data in project_data["monitors"]:
            self.monitors.append(monitor.Monitor.from_data(monitor_data))
        
        #del project_data["targets"]
        #gprint(project_data)
        
        # "targets", "monitors", "extensionData", "extensions", "meta"


file_path = "/storage/emulated/0/Git/PyPenguin/assets/from_online/my 1st platformer .pmp"
project = Project.from_pmp_file(file_path)
#gprint(project)

