from pypenguin import extractProject, compressProject, validateProject
from pypenguin.utility import Platform


optimizedData = extractProject(
#    projectFilePath          = "assets/categories/extension_music.pmp",
#    projectFilePath          = "assets/studies/assetTest.pmp",
#    projectFilePath          = "assets/from_online/The Tale of the Three Shapes.sb3",
#    projectFilePath          = "Greatest Common Division.pmp",
#    projectFilePath          = "docs/tutorials/my_project.pmp",
    projectFilePath          = "c.pmp",
    optimizedProjectDir      = "extracted_project",
    deoptimizedDebugFilePath = "temp_extracted.json",
    optimizedDebugFilePath   = "temp2.json",
    sourcePlatform           = Platform.PENGUINMOD,
    developing               = True,
)

validateProject(projectData=optimizedData)

#compressProject(
#    projectFilePath          = "export.pmp",
#    optimizedProjectDir      = "extracted_project",
#    deoptimizedDebugFilePath = "temp3.json",
#    targetPlatform=Platform.PENGUINMOD,
#)
