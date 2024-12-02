from pypenguin.database.motion    import opcodes as motion
# Looks (soon)
# Sound (soon)
from pypenguin.database.events    import opcodes as events
from pypenguin.database.control   import opcodes as control
from pypenguin.database.sensing   import opcodes as sensing
from pypenguin.database.operators import opcodes as operators
from pypenguin.database.variables import opcodes as variables
from pypenguin.database.lists     import opcodes as lists

from pypenguin.database.special   import opcodes as special
from pypenguin.database.extJSON   import opcodes as extJSON

from pypenguin.helper_functions   import ikv, flipKeysAndValues

import functools

"""
Category      Status ('.'=some 'x'=all)
    Motion    [ ]
    Looks     [ ]
    Sound     [ ]
    Events    [x]
    Control   [x]
    Sensing   [x]
    Operators [x]
    Variables [x]
    Lists     [x]
Extension     Status ('.'=some 'x'=all)
    (jg)JSON  [x]
    others aren't implemented (yet)
"""

opcodeDatabase = (
# CATEGORIES
    motion |
    # missing: Looks, Sound
    events    | control   | sensing |
    operators | variables | lists   |
    special   |
# EXTENSIONS
    extJSON
)

def getOptimizedOpcode(opcode):
    return opcodeDatabase[opcode]["newOpcode"]

@functools.cache
def getDeoptimizedOpcode(opcode):
    found = False
    for i, oldOpcode, opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == opcode:
            found = True
            break
    assert found, f"Opcode not found: {opcode}"
    return oldOpcode

def getOptimizedInputID(opcode, inputID):
    if "inputTranslation" in opcodeDatabase[opcode]:
        if inputID in opcodeDatabase[opcode]["inputTranslation"]:
            return opcodeDatabase[opcode]["inputTranslation"][inputID]
    if "menus" in opcodeDatabase[opcode]:
        for menuData in opcodeDatabase[opcode]["menus"]:
            if menuData["outer"] == inputID:
                return menuData["new"]
    return inputID

def getDeoptimizedInputID(opcode, inputID):
    if "inputTranslation" in opcodeDatabase[opcode]:
        table = flipKeysAndValues(
            opcodeDatabase[opcode]["inputTranslation"]
        )
        if inputID in table:
            return table[inputID]
    if "menus" in opcodeDatabase[opcode]:
        for menuData in opcodeDatabase[opcode]["menus"]:
            if menuData["new"] == inputID:
                return menuData["outer"]
    return inputID

def getInputType(opcode, inputID):
    return opcodeDatabase[opcode]["inputTypes"][inputID]

def getInputTypes(opcode):
    return opcodeDatabase[opcode]["inputTypes"]

def getInputMode(opcode, inputID):
    return inputModes[getInputType(
        opcode=opcode, 
        inputID=inputID,
    )]

def getInputModes(opcode):
    return {inputID: getInputMode(
        opcode=opcode,
        inputID=inputID,
    ) for inputID in getInputTypes(opcode).keys()}

def getOptimizedOptionID(opcode, optionID):
    if "optionTranslation" not in opcodeDatabase[opcode]:
        return optionID
    if optionID not in opcodeDatabase[opcode]["optionTranslation"]:
        return optionID
    return opcodeDatabase[opcode]["optionTranslation"][optionID]

def getDeoptimizedOptionID(opcode, optionID):
    if "optionTranslation" in opcodeDatabase[opcode]:
        table = flipKeysAndValues(
            opcodeDatabase[opcode]["optionTranslation"]
        )
        if optionID in table:
            return table[optionID]
    if "menus" in opcodeDatabase[opcode]:
        for menuData in opcodeDatabase[opcode]["menus"]:
            if menuData["new"] == optionID:
                return menuData["inner"]
    return optionID

def getBlockType(opcode):
    return opcodeDatabase[opcode]["type"]

def getMenu(opcode, inputID):
    if "menus" not in opcodeDatabase[opcode]:
        return None
    for menu in opcodeDatabase[opcode]["menus"]:
        if menu["new"] == inputID:
            return menu
    return None

def getInputMagicNumber(inputType):
    match inputType:
        case "broadcast"       : magicNumber = 11
        case "text"            : magicNumber = 10
        case "color"           : magicNumber =  9
        case "direction"       : magicNumber =  8
        case "integer"         : magicNumber =  7
        case "positive integer": magicNumber =  6
        case "positive number" : magicNumber =  5
        case "number"          : magicNumber =  4
        case "boolean"         : pass
    return magicNumber

def getOptionType(opcode, optionID):
    return opcodeDatabase[opcode]["optionTypes"][optionID]

def getOptionTypes(opcode):
    return opcodeDatabase[opcode]["optionTypes"]

inputDefault = {}
inputBlockDefault = None
inputTextDefault = ""
inputBlocksDefault = []
optionDefault = {}
commentDefault = None

inputModes = {
    "direction"       : "block-and-text",
    "integer"         : "block-and-text",
    "positive integer": "block-and-text",
    "positive number" : "block-and-text",
    "number"          : "block-and-text",
    "text"            : "block-and-text",
    "color"           : "block-and-text",
    "boolean"         : "block-only",
    "round"           : "block-only",
    "script"          : "script",

    "broadcast"                      : "block-and-hybrid-option",
    "other sprite or stage"          : "block-and-option",
    "cloning target"                 : "block-and-option",
    "exclusive touchable object"     : "block-and-option",
    "half-inclusive touchable object": "block-and-option",
    "inclusive touchable object"     : "block-and-option",
    "touchable sprite"               : "block-and-option",
    "key"                            : "block-and-option",
    "up or down"                     : "block-and-option",
    "finger index"                   : "block-and-option",
    "reachable target"               : "block-and-option",
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
