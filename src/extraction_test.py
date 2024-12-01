from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
    projectFilePath     = "assets/categories/sensing.pmp",
    #projectFilePath     = "assets/studies/proceduresDef.pmp",
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
