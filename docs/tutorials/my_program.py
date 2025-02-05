import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))


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

project_directory = "my_project_directory" # The name of the directory, you just created.
penguinmod_file   = "my_project.pmp" # The file path of the PenguinMod Project, that will be created.
target_platform   = pypenguin.Platform.PENGUINMOD # Our target platform. May also be Platform.SCRATCH.

# Update the project data
myStage  = pypenguin.defaultStage
mySprite = pypenguin.defaultSprite
mySprite["scripts"] = generated_scripts # Include the generated scripts.

mySprite["sounds"] = [pypenguin.downloadSound(
    name             = "Squawk",
    projectDirectory = project_directory,
    spriteName       = "Sprite1",
    spriteIsStage    = False,
    fileName         = "Squawk",
    doOverwrite      = True,
), pypenguin.downloadSound(
    name             = "Splash Cymbal",
    projectDirectory = project_directory,
    spriteName       = "Sprite1",
    spriteIsStage    = False,
    fileName         = "Splash Cymbal",
    doOverwrite      = True,
), pypenguin.downloadSound(
    name             = "Pop",
    projectDirectory = project_directory,
    spriteName       = "Sprite1",
    spriteIsStage    = False,
    fileName         = "Pop",
    doOverwrite      = True,
), pypenguin.downloadSound(
    name             = "Pralax",
    projectDirectory = project_directory,
    spriteName       = "Sprite1",
    spriteIsStage    = False,
    fileName         = "Pralax",
    doOverwrite      = True,
)]


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
)