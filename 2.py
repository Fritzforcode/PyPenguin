from src.pypenguin import extractAndOptimizeProject
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/pypenguin')))
extractAndOptimizeProject(
        projectFilePath           = "assets/categories/variables and lists.pmp",
        optimizedProjectDirectory = "optimizedProject/",
        temporaryDirectory        = "temporary/",
    )