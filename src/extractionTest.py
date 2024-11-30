from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
    #projectFilePath           = "assets/categories/sensing_p3.pmp",
    projectFilePath           = "assets/studies/commentTest.pmp",
    optimizedProjectDirectory = "extractedProject",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)

validateProject(projectData=optimizedData)

deoptimizeAndCompressProject(
    projectFilePath           = "export.pmp",
    optimizedProjectDirectory = "extractedProject",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)
