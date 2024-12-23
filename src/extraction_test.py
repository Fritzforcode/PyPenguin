from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
#    projectFilePath          = "assets/categories/extBitwise.pmp",
    projectFilePath          = "assets/studies/correction.pmp",
#    projectFilePath          = "assets/from_online/my 1st platformer .pmp",
    optimizedProjectDir      = "extracted_project",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp_correct.json",
#    optimizedDebugFilePath   = "temp2.json",
)

#validateProject(projectData=optimizedData)

#deoptimizeAndCompressProject(
#    projectFilePath          = "export.pmp",
#    optimizedProjectDir      = "extracted_project",
#    temporaryDir             = "temporary",
#    deoptimizedDebugFilePath = "temp3.json"
#)
