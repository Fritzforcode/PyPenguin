from src.pypenguin import extractAndOptimizeProject, deoptimizeAndCompressProject
extractAndOptimizeProject(
    projectFilePath="assets/studies/ifBlock2.pmp",
    optimizedProjectDirectory="extractedProject",
    temporaryDirectory="temporary",
)
deoptimizeAndCompressProject(
    projectFilePath="export.pmp",
    optimizedProjectDirectory="extractedProject",
    temporaryDirectory="temporary",
)

