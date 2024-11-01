from source_extractor import extractProject

extractProject(
    pmpFilePath="assets/studies/soundTest.pmp",
    jsonFilePath="assets/project.json",
    temporaryDir="temporary/",
    deleteTemporaryDir=True,
)
