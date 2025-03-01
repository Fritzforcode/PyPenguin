import pypenguin
import json
import os # For convenience and creating a dir
import utility

project_directory = utility.ensureCorrectPath("btt", "PyPenguin")
penguinmod_file   = "export.pmp"
target_platform   = pypenguin.Platform.PENGUINMOD

# Parse scratchblocks text
with open(utility.ensureCorrectPath("src/code.txt", "PyPenguin")) as file:
    main_block_text = file.read()

console_block_text = """
when flag clicked
show sprite
go to x: [0] y: [150]
set font to [Monospace]
set text color to [#000000]
set width to [450] aligned [left v]

when i receive [refresh v]
show text (.CONSOLE)
"""

main_scripts    = pypenguin.parseBlockText(main_block_text)
console_scripts = pypenguin.parseBlockText(console_block_text)

# Update the project data
my_stage  = pypenguin.defaultStage
main_sprite = pypenguin.defaultSprite.copy()
main_sprite["scripts"] = main_scripts # Include the generated scripts.
main_sprite["name"] = "main"
console_sprite = pypenguin.defaultSprite.copy()
console_sprite["scripts"] = console_scripts
console_sprite["name"] = "console"

project = pypenguin.defaultProject
project["sprites"] = [  # Update project with the modified sprites.
    my_stage,
    main_sprite,
    console_sprite,
]

globalVariables = ["ADDRESSING", "OPCODES", "BYTEORDER", "PAGE_WRAPPING_BUG", "ROM_START", "KERNAL_CHROUT_ADDRESS", "ASCII_MAPPING", ".CONSOLE"]

project["globalVariables"] = [{"name": name, "currentValue": "", "isCloudVariable": False} for name in globalVariables]
project["extensions"     ] = ["jgJSON", "lmsTempVars2", "Bitwise", "text"]
project["extensionURLs"] = {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}

# Create our project directory
if not os.path.exists(project_directory):
    os.makedirs(project_directory, exist_ok=True)

# Write our project data to project.json
with open(os.path.join(project_directory, "project.json"), "w") as file_object:
    json.dump(project, file_object) 


# Make sure our project is valid. The Validator is NOT perfect!
# If the project is invalid, an Exception will be raised.
#pp(project)
pypenguin.validateProject(project)


# Compress our project from a directory to a Project.
pypenguin.compressProject(
    optimizedProjectDir = project_directory,
    projectFilePath     = penguinmod_file, 
    targetPlatform      = target_platform,
    deoptimizedDebugFilePath="t_deop.json",
    developing          = True,
)



