from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
    projectFilePath           = "assets/categories/control.pmp",#studies/test.pmp",
    optimizedProjectDirectory = "extractedProject",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)

validateProject(projectData=optimizedData)

#deoptimizeAndCompressProject(
#    projectFilePath           = "export.pmp",
#    optimizedProjectDirectory = "extractedProject",
#    temporaryDirectory        = "temporary",
#    writeDebugFiles           = True,
#)
