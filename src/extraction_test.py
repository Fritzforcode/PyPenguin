from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.helper_functions import readJSONFile, pp, Platform

optimizedData = extractAndOptimizeProject(
#    projectFilePath          = "assets/categories/extension_files.pmp",
#    projectFilePath          = "assets/studies/pen.pmp",
    projectFilePath          = "assets/from_online/The Tale of the Three Shapes.sb3",
    optimizedProjectDir      = "tale",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp_extracted.json",
    optimizedDebugFilePath   = "temp2.json",
    sourcePlatform           = Platform.SCRATCH,
)

validateProject(projectData=optimizedData)

#deoptimizeAndCompressProject(
#    projectFilePath          = "export.pmp",
#    optimizedProjectDir      = "extracted_project",
#    temporaryDir             = "temporary",
#    deoptimizedDebugFilePath = "temp3.json"
#)
