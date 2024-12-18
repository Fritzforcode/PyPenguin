from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp

optimizedData = extractAndOptimizeProject(
#    projectFilePath          = "assets/categories/custom_blocks.pmp",
    projectFilePath          = "assets/studies/motionOptions.pmp",
#    projectFilePath          = "assets/from_online/my 1st platformer .pmp",
    optimizedProjectDir      = "extracted_project",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp1.json",
    optimizedDebugFilePath   = "temp2.json",
)

validateProject(projectData=optimizedData)

deoptimizeAndCompressProject(
    projectFilePath          = "export.pmp",
    optimizedProjectDir      = "extracted_project",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp3.json"
)
