import sys,os;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from pypenguin.database import getAllDeoptimizedOpcodes, getOptimizedOpcode, getBlockCategory, getInputModes
from pypenguin.helper_functions import pp, insureCorrectPath

def toFileId(string: str):
    return (string.lower()
        .replace("(","").replace(")", "")
        .replace("[","").replace("]", "")
        .replace("{","").replace("}", "")
        .replace("<","").replace(">", "")
        .replace(" ", "-").replace(":", "")
    )

allOpcodes = getAllDeoptimizedOpcodes()
output = ""
lastCategory = None
for opcode in allOpcodes[:25]:
    newOpcode = getOptimizedOpcode(opcode=opcode)
    blockFileId = toFileId(newOpcode) + ".png" # TODO: add exceptions
    category = getBlockCategory(opcode=opcode)
    filePath = os.path.join("blocks", toFileId(category), blockFileId)
    inputModes = getInputModes(opcode=opcode)

    globalPath = insureCorrectPath(
        os.path.join("automation", filePath),
        "PyPenguin",
    )
    if not os.path.exists(globalPath):
        print("-", blockFileId.removesuffix(".png"))

    if category != lastCategory:
        output += f"# {category}\n"
        lastCategory = category
    
    output += f'![]({filePath})  \n'
    output += f'**`"{newOpcode}"`**:\n'
    for inputId, inputMode in inputModes.items():
        output += f'  * `"{inputId}"`: `"{inputMode}"`\n'
    output += "## \n"


with open(insureCorrectPath("automation/out.md", "PyPenguin"), "w") as file:
    file.write(output)
