from src.pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject
extractAndOptimizeProject(
    projectFilePath="assets/studies/ifBlock.pmp",
    optimizedProjectDirectory="extractedProject",
    temporaryDirectory="temporary",
)
#deoptimizeAndCompressProject(
#    projectFilePath="export.pmp",
#    optimizedProjectDirectory="extractedProject",
#    temporaryDirectory="temporary",
#)

