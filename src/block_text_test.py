import pypenguin
import json
import os # For convenience and creating a dir

# Parse scratchblocks text
block_text = """
define define () //{"blockType": "textReporter", "comment": "abfdasd djk "}
"""
generated_scripts = pypenguin.parseBlockText(block_text)

project_directory = pypenguin.utility.ensureCorrectPath("btt", "PyPenguin")
penguinmod_file   = "export.pmp"
target_platform   = pypenguin.Platform.PENGUINMOD

# Update the project data
myStage  = pypenguin.defaultStage
mySprite = pypenguin.defaultSprite
mySprite["scripts"] = generated_scripts # Include the generated scripts.

project = pypenguin.defaultProject
project["sprites"] = [  # Update project with the modified sprites.
    myStage,
    mySprite,
]


# Create our project directory
if not os.path.exists(project_directory):
    os.makedirs(project_directory, exist_ok=True)

# Write our project data to project.json
with open(os.path.join(project_directory, "project.json"), "w") as file_object:
    json.dump(project, file_object) 


# Make sure our project is valid. The Validator is NOT perfect!
# If the project is invalid, an Exception will be raised.
pypenguin.validateProject(project)


# Compress our project from a directory to a Project.
pypenguin.compressProject(
    optimizedProjectDir = project_directory,
    projectFilePath     = penguinmod_file, 
    targetPlatform      = target_platform,
    deoptimizedDebugFilePath="t_deop.json",
    developing          = True,
)



