from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.utility import pp

optimizedData = extractAndOptimizeProject(
    projectFilePath           = "assets/studies/test2.pmp",
    optimizedProjectDirectory = "extracted_project",
    temporaryDirectory        = "temporary",
    deoptimizedDebugFilePath  = "temp1.json",
    optimizedDebugFilePath    = "temp2.json",
)

validateProject(projectData=optimizedData)


"""from pypenguin.deoptimize.blocks_scripts import unfinishScripts, flattenScripts, unprepareBlocks
scriptDatas           = optimizedData["sprites"][1]["scripts"]
unfinishedScriptDatas = unfinishScripts(scriptDatas)
flattendScriptDatas   = flattenScripts(unfinishedScriptDatas)
pp(unprepareBlocks(data=flattendScriptDatas))
"""

deoptimizeAndCompressProject(
    projectFilePath           = "export.pmp",
    optimizedProjectDirectory = "extracted_project",
    temporaryDirectory        = "temporary",
    deoptimizedDebugFilePath  = "temp3.json"
)
