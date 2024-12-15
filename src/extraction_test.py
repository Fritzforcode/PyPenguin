from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
#    projectFilePath     = "assets/categories/control.pmp",
    projectFilePath     = "assets/studies/pop.pmp",
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
