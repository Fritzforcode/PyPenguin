### [Back: Introduction](introduction.md)

# Hello World
We will create a project, that asks the user his name and welcomes him. 
If the user's name is "Skywalker", the project will reply "I don't like sand too!".

## Steps
1. Parse [scratchblocks text](https://scratchblocks.github.io/#?style=scratch3&script=when%20green%20flag%20clicked%0Asay%20%5BHello%20World!%5D%20for%20(2)%20secs%0Aask%20%5BWhat's%20your%20name%3F%5D%20and%20wait%0Aif%20%3C(answer)%20%3D%20%5BSkywalker%5D%3E%20then%0A%09say%20%5BI%20don't%20like%20sand%20too!%5D%20for%20(2)%20secs%0Aend%0Asay%20(join%20%5BWelcome%2C%20%5D%20(answer))%20for%20(2)%20secs) into scripts.
    ```py
    # Parse scratchblocks text
    block_text = """
    when green flag clicked
    say [Hello World!] for (2) secs
    ask [What's your name?] and wait
    if <(answer) = [Skywalker]> then
        say [I don't like sand too!] for (2) secs
    end
    say (join [Welcome, ] (answer)) for (2) secs
    """
    generated_scripts = pypenguin.parseBlockText(block_text)
    ```
2. Update the project data to the generated scripts.
    ```py
    # Update the project data
    myStage  = pypenguin.defaultStage
    mySprite = pypenguin.defaultSprite
    mySprite["scripts"] = generated_scripts # Include the generated scripts.

    project = pypenguin.defaultProject
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
when green flag clicked
say [Hello World!] for (2) secs
ask [What's your name?] and wait
if <(answer) = [Skywalker]> then
    say [I don't like sand too!] for (2) secs
end
say (join [Welcome, ] (answer)) for (2) secs
"""
generated_scripts = pypenguin.parseBlockText(block_text)


# Update the project data
myStage  = pypenguin.defaultStage
mySprite = pypenguin.defaultSprite
mySprite["scripts"] = generated_scripts # Include the generated scripts.

project = pypenguin.defaultProject
project["sprites"] = [  # Update project with the modified sprites.
    myStage,
    mySprite,
]


project_directory = "my_project_directory/" # The name of the directory, you just created.
penguinmod_file   = "my_project.pmp" # The file path of the PenguinMod Project, that will be created.
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


# Compress our project from a directory to a Project.
pypenguin.compressProject(
    optimizedProjectDir = project_directory,
    projectFilePath     = penguinmod_file, 
    targetPlatform      = target_platform,
)
```

## Done
You can now open our project in the [**PenguinMod Editor**](https://studio.penguinmod.com/editor.html).

### [Next: Adding Assets](adding_assets.md)

