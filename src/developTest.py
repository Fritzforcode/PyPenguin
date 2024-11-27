from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
    projectFilePath           = "assets/studies/inputTest.pmp",#test2.pmp",
    optimizedProjectDirectory = "extractedProject",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)

validateProject(projectData=optimizedData)


from pypenguin.deoptimize.blocks_scripts import unfinishScripts, flattenScripts, unprepareBlocks
scriptDatas           = optimizedData["sprites"][1]["scripts"]
unfinishedScriptDatas = unfinishScripts(scriptDatas)
flattendScriptDatas   = flattenScripts(unfinishedScriptDatas)
pp(unprepareBlocks(data=flattendScriptDatas))

"""
deoptimizeAndCompressProject(
    projectFilePath           = "../export.pmp",
    optimizedProjectDirectory = "../extractedProject",
    temporaryDirectory        = "../temporary",
    writeDebugFiles           = True,
)
"""