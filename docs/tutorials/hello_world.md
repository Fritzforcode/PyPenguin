### [Back: Introduction](introduction.md)

# Hello World
## Steps
1. Parse scratchblocks text into scripts.
```py
# Parse scratchblocks text
block_text = """
say [Hello World!] for 2 secs
"""
generated_scripts = pypenguin.parseBlockText(block_text)
```
2. Update the project data to the generated scripts.
``` py
# Update the project data
myStage  = pypenguin.database.defaultStage
mySprite = pypenguin.database.defaultSprite
mySprite["scripts"] = generated_scripts # Include the generated scripts.

project = pypenguin.database.defaultProject
project["sprites"] = [  # Update project with the modified sprites.
    myStage,
    mySprite,
]
```
## Full Program

```py
# my_program.py
import pypenguin
import json
import os # For convenience and creating a dir

# Parse scratchblocks text
block_text = """
say [Hello World!] for 2 secs
"""
generated_scripts = pypenguin.parseBlockText(block_text)


# Update the project data
myStage  = pypenguin.database.defaultStage
mySprite = pypenguin.database.defaultSprite
mySprite["scripts"] = generated_scripts # Include the generated scripts.

project = pypenguin.database.defaultProject
project["sprites"] = [  # Update project with the modified sprites.
    myStage,
    mySprite,
]


project_directory = "my_project_directory/" # The name of the directory, you just created.
penguinmod_file   = "my_project.pmp" # The file path of the PenguinMod Project, that will be created.
target_platform   = pypenguin.Platform.PENGUINMOD # Your target platform. May also be Platform.SCRATCH.

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
)
```

## Done
You can now open your project in the **PenguinMod Edtor**.

### [Next: Hello World](hello_world.md)

