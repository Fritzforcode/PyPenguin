# Introduction
In this tutorial, we will set up the development environment and create your first project.
## Installation

### Prerequisites
Make sure you have Python installed. If you don't have it yet, download and install it from [python.org](https://www.python.org/downloads/).

### Install PyPenguin
Once Python is installed, you can install PyPenguin using pip:

```sh
pip install pypenguin
```

## Your first project
1. Create a new python file eg. ˋmy_program.pyˋ
2. import **pypenguin** and **json** (for writing json files)
    ```py
    import pypenguin
    import json # For writing JSON Files
    import os # For convenience and creating a dir
    ```
3. Generate the project data.
    ```py
    myStage  = pypenguin.defaultStage
    mySprite = pypenguin.defaultSprite

    project = pypenguin.defaultProject
    project["sprites"] = [  # Update project with the new sprites. We will modify them in the future.
        myStage,
        mySprite,
    ]
    ```
4. Create a directory. It will contain all costume files, sound files and **project.json**. **project.json** will describe the contents of our **PenguinMod Project**.
    ```py
    project_directory = "my_project_directory/" # The name of the directory, you just created.
    penguinmod_file   = "my_project.pmp" # The file path of the PenguinMod Project, that will be created.
    target_platform   = pypenguin.Platform.PENGUINMOD # Our target platform. May also be Platform.SCRATCH.

    # Create our project directory
    if not os.path.exists(project_directory):
        os.makedirs(project_directory, exist_ok=True)
    ```
5. Validate and compress our **PenguinMod Project**.
    ```py
    # Write our project data to project.json
    with open(os.path.join(project_directory, "project.json"), "w") as file_object:
        json.dump(project, file_object) 

    # Make sure our project is valid. The Validator is NOT perfect!
    # If the project is invalid, an Exception will be raised.
    pypenguin.validateProject(project)



    # Compress our project from a directory to a PenguinMod Project
    pypenguin.compressProject(
        optimizedProjectDir = project_directory,
        projectFilePath     = penguinmod_file, 
        targetPlatform      = target_platform,
    )
    ```

### Full Program
```py
import pypenguin
import json # For writing JSON Files
import os # For convenience and creating a dir

# Create the project data
myStage  = pypenguin.defaultStage
mySprite = pypenguin.defaultSprite

project = pypenguin.defaultProject
project["sprites"] = [  # Update project with the new sprites. We will modify them in the future.
    myStage,
    mySprite,
]



project_directory = "my_project_directory/" # The name of the directory, you just created.
penguinmod_file   = "my_project.pmp" # The file path of the PenguinMod Project, that will be created.     Change this to [...].sb3 for Scratch Projects.
target_platform   = pypenguin.Platform.PENGUINMOD # Our target platform. May also be Platform.SCRATCH.

# Create our project directory
if not os.path.exists(project_directory):
    os.makedirs(project_directory, exist_ok=True)


# Write our project data to project.json
with open(os.path.join(project_directory, "project.json"), "w") as file_object:
    json.dump(project, file_object) 

# Make sure our project is valid. The Validator is NOT perfect!
# If the project is invalid, an Exception will be raised.
pypenguin.validateProject(project)



# Compress our project from a directory to a Project
pypenguin.compressProject(
    optimizedProjectDir = project_directory,
    projectFilePath     = penguinmod_file, 
    targetPlatform      = target_platform,
)
```

## Done
You can now upload our project in the [**PenguinMod Editor**](https://studio.penguinmod.com/editor.html).
1. Open the [**PenguinMod Editor**](https://studio.penguinmod.com/editor.html).
2. In the top left corner click **File** and **Load from our computer**
3. Choose our generated ˋ.pmpˋ/ˋ.sb3ˋ file.
You can now view our empty project.

### [Next: Hello World](hello_world.md)
