from pypenguin.database.events    import opcodes as events
from pypenguin.database.control   import opcodes as control
from pypenguin.database.operators import opcodes as operators
from pypenguin.database.variables import opcodes as variables
from pypenguin.database.lists     import opcodes as lists

from pypenguin.database.special   import opcodes as special

from pypenguin.database.extJSON   import opcodes as extJSON

"""
Category      Status ('.'=some 'x'=all)
    Motion    [ ]
    Looks     [ ]
    Sound     [ ]
    Events    [.]
    Control   [x]
    Sensing   [ ]
    Operators [x]
    Variables [x]
    Lists     [x]
Extension     Status ('.'=some 'x'=all)
    (jg)JSON  [x]
    others aren't implemented
"""

opcodeDatabase = (
# CATEGORIES
    # missing: Motion, Looks, Sound
    events | control | 
    # missing: Sensing
    operators | variables | lists |
    special |
# EXTENSIONS
    extJSON
)

inputDefault = {}
inputBlockDefault = None
inputTextDefault = ""
inputBlocksDefault = []
optionDefault = {}
commentDefault = None

inputModes = {
    "broadcast"       : "block-and-text",
    "integer"         : "block-and-text",
    "positive integer": "block-and-text",
    "positive number" : "block-and-text",
    "number"          : "block-and-text",
    "text"            : "block-and-text",
    "boolean"         : "block-only",
    "round"           : "block-only",
    "script"          : "script",
}


defaultCostume = {
    "name": "empty costume",
    "dataFormat": "svg",
    "fileStem": "cd21514d0531fdffb22204e0ec5ed84a",
    "bitmapResolution": 1,
    "rotationCenter": [0, 0]
}

defaultCostumeDeoptimized = {
    "name": "empty costume",
    "bitmapResolution": 1,
    "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
    "dataFormat": "svg",
    "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
    "rotationCenterX": 0,
    "rotationCenterY": 0
}

defaultCostumeFilePath = "assets/defaultCostume.svg"
