from src.pypenguin import extractAndOptimizeProject, validateProject
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/pypenguin')))
optimizedData = extractAndOptimizeProject(
        projectFilePath           = "assets/studies/varBlockTest.pmp",
        optimizedProjectDirectory = "optimizedProject/",
        temporaryDirectory        = "temporary/",
    )
validateProject(projectData=optimizedData)