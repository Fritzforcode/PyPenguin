from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile
optimizedData = extractAndOptimizeProject(
    projectFilePath="assets/studies/proceduresDef.pmp",
    optimizedProjectDirectory="extractedProject",
    temporaryDirectory="temporary",
    writeDebugFiles=False,
)

validateProject(projectData=optimizedData)

#deoptimizeAndCompressProject(
#    projectFilePath="export.pmp",
#    optimizedProjectDirectory="extractedProject",
#    temporaryDirectory="temporary",
#)

