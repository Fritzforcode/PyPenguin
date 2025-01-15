from pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject, validateProject
from pypenguin.utility import Platform

# Import time module
import time
 
# record start time
start = time.time()

optimizedData = extractAndOptimizeProject(
#    projectFilePath          = "assets/categories/extension_files.pmp",
    projectFilePath          = "assets/studies/commentTest.pmp",
#    projectFilePath          = "assets/from_online/The Tale of the Three Shapes.sb3",
    optimizedProjectDir      = "tale",
    temporaryDir             = "temporary",
    deoptimizedDebugFilePath = "temp_extracted.json",
    optimizedDebugFilePath   = "temp2.json",
    sourcePlatform           = Platform.PENGUINMOD,
)

validateProject(projectData=optimizedData)

end = time.time()
print("The time of execution of above program is :", (end-start) * 10**3, "ms")

#deoptimizeAndCompressProject(
#    projectFilePath          = "export.pmp",
#    optimizedProjectDir      = "extracted_project",
#    temporaryDir             = "temporary",
#    deoptimizedDebugFilePath = "temp3.json"
#)
