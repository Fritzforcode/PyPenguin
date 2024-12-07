from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
    projectFilePath     = "assets/categories/variables and lists.pmp",
#    projectFilePath     = "assets/studies/monitors2.pmp",
#    projectFilePath     = "assets/from_online/my 1st platformer .pmp",
    optimizedProjectDir = "extractedProject",
    temporaryDir        = "temporary",
    writeDebugFiles     = True,
)

validateProject(projectData=optimizedData)

deoptimizeAndCompressProject(
    projectFilePath     = "export.pmp",
    optimizedProjectDir = "extractedProject",
    temporaryDir        = "temporary",
    writeDebugFiles     = True,
)
# temporary helper script https://pastebin.com/V3s9qWmE
