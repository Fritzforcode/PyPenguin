from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp
optimizedData = extractAndOptimizeProject(
    projectFilePath           = "assets/studies/switches.pmp",
    optimizedProjectDirectory = "extractedProject",
    temporaryDirectory        = "temporary",
    writeDebugFiles           = True,
)
pp(optimizedData)
#validateProject(projectData=optimizedData)

#deoptimizeAndCompressProject(
#    projectFilePath           = "export.pmp",
#    optimizedProjectDirectory = "extractedProject",
#    temporaryDirectory        = "temporary",
#    writeDebugFiles           = True,
#)

