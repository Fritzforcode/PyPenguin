import pypenguin
import json
import os # For convenience and creating a dir
from pypenguin.utility import pp
# Parse scratchblocks text
with open(pypenguin.utility.ensureCorrectPath("src/code.txt", "PyPenguin")) as file:
    block_text = file.read()
block_text = """when flag clicked
set [ADDRESSING v] to [\["imp", "inx", "   ", "   ", "   ", "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "   ", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ", "abs", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "abs", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ", "imp", "inx", "   ", "   ", "   ", "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "abs", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ", "imp", "inx", "   ", "   ", "   ", "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "ind", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ", "   ", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "   ", "imp", "   ", "abs", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "zpx", "zpx", "zpy", "   ", "imp", "aby", "imp", "   ", "   ", "abx", "   ", "   ", "imm", "inx", "imm", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "imp", "   ", "abs", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "zpx", "zpx", "zpy", "   ", "imp", "aby", "imp", "   ", "abx", "abx", "aby", "   ", "imm", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "imp", "   ", "abs", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ", "imm", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "imp", "   ", "abs", "abs", "abs", "   ", "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   "\]]
set [OPCODES v] to [\["brk", "ora", "   ", "   ", "   ", "ora", "asl", "   ", "php", "ora", "asl", "   ", "   ", "ora", "asl", "   ", "bpl", "ora", "   ", "   ", "   ", "ora", "asl", "   ", "clc", "ora", "   ", "   ", "   ", "ora", "asl", "   ", "jsr", "and", "   ", "   ", "bit", "and", "rol", "   ", "plp", "and", "rol", "   ", "bit", "and", "rol", "   ", "bmi", "and", "   ", "   ", "   ", "and", "rol", "   ", "sec", "and", "   ", "   ", "   ", "and", "rol", "   ", "rti", "eor", "   ", "   ", "   ", "eor", "lsr", "   ", "pha", "eor", "lsr", "   ", "jmp", "eor", "lsr", "   ", "bvc", "eor", "   ", "   ", "   ", "eor", "lsr", "   ", "cli", "eor", "   ", "   ", "   ", "eor", "lsr", "   ", "rts", "adc", "   ", "   ", "   ", "adc", "ror", "   ", "pla", "adc", "ror", "   ", "jmp", "adc", "ror", "   ", "bvs", "adc", "   ", "   ", "   ", "adc", "ror", "   ", "sei", "adc", "   ", "   ", "   ", "adc", "ror", "   ", "   ", "sta", "   ", "   ", "sty", "sta", "stx", "   ", "dey", "   ", "txa", "   ", "sty", "sta", "stx", "   ", "bcc", "sta", "   ", "   ", "sty", "sta", "stx", "   ", "tya", "sta", "txs", "   ", "   ", "sta", "   ", "   ", "ldy", "lda", "ldx", "   ", "ldy", "lda", "ldx", "   ", "tay", "lda", "tax", "   ", "ldy", "lda", "ldx", "   ", "bcs", "lda", "   ", "   ", "ldy", "lda", "ldx", "   ", "clv", "lda", "tsx", "   ", "ldy", "lda", "ldx", "   ", "cpy", "cmp", "   ", "   ", "cpy", "cmp", "dec", "   ", "iny", "cmp", "dex", "   ", "cpy", "cmp", "dec", "   ", "bne", "cmp", "   ", "   ", "   ", "cmp", "dec", "   ", "cld", "cmp", "   ", "   ", "   ", "cmp", "dec", "   ", "cpx", "sbc", "   ", "   ", "cpx", "sbc", "inc", "   ", "inx", "sbc", "nop", "   ", "cpx", "sbc", "inc", "   ", "beq", "sbc", "   ", "   ", "   ", "sbc", "inc", "   ", "sed", "sbc", "   ", "   ", "   ", "sbc", "inc", "   "\]]
set [BYTEORDER v] to [little]

"""

globalVariables = ["ADDRESSING", "OPCODES", "BYTEORDER", "PAGE_WRAPPING_BUG"]

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

project["globalVariables"] = [{"name": name, "currentValue": "", "isCloudVariable": False} for name in globalVariables]
project["extensions"     ] = ["jgJSON", "lmsTempVars2", "Bitwise"]
project["extensionURLs"] = {"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}

# Create our project directory
if not os.path.exists(project_directory):
    os.makedirs(project_directory, exist_ok=True)

# Write our project data to project.json
with open(os.path.join(project_directory, "project.json"), "w") as file_object:
    json.dump(project, file_object) 


# Make sure our project is valid. The Validator is NOT perfect!
# If the project is invalid, an Exception will be raised.
pp(project)
pypenguin.validateProject(project)


# Compress our project from a directory to a Project.
pypenguin.compressProject(
    optimizedProjectDir = project_directory,
    projectFilePath     = penguinmod_file, 
    targetPlatform      = target_platform,
    deoptimizedDebugFilePath="t_deop.json",
    developing          = True,
)



