from pypenguin.database.motion    import opcodes as motion
from pypenguin.database.looks     import opcodes as looks
from pypenguin.database.sounds    import opcodes as sounds
from pypenguin.database.events    import opcodes as events
from pypenguin.database.control   import opcodes as control
from pypenguin.database.sensing   import opcodes as sensing
from pypenguin.database.operators import opcodes as operators
from pypenguin.database.variables import opcodes as variables
from pypenguin.database.lists     import opcodes as lists

from pypenguin.database.special   import opcodes as special
from pypenguin.database.extJSON   import opcodes as extJSON

from pypenguin.helper_functions   import ikv, pp, flipKeysAndValues, removeDuplicates

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
    motion    | looks     | sounds  |
    events    | control   | sensing |
    operators | variables | lists   |
    special   |
# EXTENSIONS
    extJSON
)

def getAllDeoptimizedOpcodes():
    return [opcode for opcode in opcodeDatabase.keys()]

def getAllOptimizedOpcodes():
    opcodes = {}
    for i, oldOpcode, opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] in opcodes.values():
            index       = list(opcodes.values()).index(opcodeData["newOpcode"])
            otherOpcode = list(opcodes.keys  ())[index]
            raise Exception(f"Double opocde detected {otherOpcode} and {oldOpcode}")
        opcodes[oldOpcode] = opcodeData["newOpcode"]
    return list(opcodes.values())

def getAllMonitorOpcodes():
    opcodes = {}
    for i, oldOpcode, opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] in opcodes.values():
            index       = list(opcodes.values()).index(opcodeData["newOpcode"])
            otherOpcode = list(opcodes.keys  ())[index]
            raise Exception(f"Double opocde detected {otherOpcode} and {oldOpcode}")
        
        if opcodeData.get("canHaveMonitor") == True:
            opcodes[oldOpcode] = opcodeData["newOpcode"]
    return list(opcodes.values())

def getOptimizedOpcode(opcode):
    return opcodeDatabase[opcode]["newOpcode"]

@functools.cache
def getDeoptimizedOpcode(opcode):
    found = False
    for i, oldOpcode, opcodeData in ikv(opcodeDatabase):
        if opcodeData["newOpcode"] == opcode:
            found = True
            break
    assert found, f"Opcode not found    : {opcode}"
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

def getPredefinedTokens(opcode):
    return opcodeDatabase[opcode].get("tokens", None)

def getInputType(opcode, inputID):
    try:
        return opcodeDatabase[opcode]["inputTypes"][inputID]
    except KeyError:
        raise Exception(f"Could not find input '{inputID}' for a block with opcode '{opcode}'")

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
    print(opcode, optionID)
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

    "broadcast"                           : "block-and-hybrid-option",
    "stage || other sprite"               : "block-and-option",
    "cloning target"                      : "block-and-option",
    "mouse || other sprite"               : "block-and-option",
    "mouse|edge || other sprite"          : "block-and-option",
    "mouse|edge || myself || other sprite": "block-and-option",
    "key"                                 : "block-and-option",
    "up|down"                             : "block-and-option",
    "finger index"                        : "block-and-option",
    "random|mouse || other sprite"        : "block-and-option",
    "costume"                             : "block-and-option",
    "costume property"                    : "block-and-option",
    "backdrop"                            : "block-and-option",
    "backdrop property"                   : "block-and-option",
    "myself || other sprite"              : "block-and-option",
    "sound"                               : "block-and-option",
}

optionTypeDatabase = {
    "key": {
        "directValues"   : [
            "space", "up arrow", "down arrow", "right arrow", "left arrow", 
            "enter", "any", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
            "x", "y", "z", "-", ",", ".", "`", "=", "[", "]", "\\", ";", "'", 
            "/", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", 
            "{", "}", "|", ":", '"', "?", "<", ">", "~", "backspace", "delete", 
            "shift", "caps lock", "scroll lock", "control", "escape", "insert", 
            "home", "end", "page up", "page down",
        ], 
        "valueSegments"  : [],
    },
    "unary math operation": {
        "directValues"   : ["abs", "floor", "ceiling", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "ln", "log", "e ^", "10 ^"], 
        "valueSegments"  : [],
    },
    "power|root|log": {
        "directValues"   : ["^", "root", "log"], 
        "valueSegments"  : [],
    },
    "root|log": {
        "directValues"   : ["root", "log"], 
        "valueSegments"  : [],
    },
    "text method": {
        "directValues"   : ["starts", "ends"], 
        "valueSegments"  : [],
    },
    "text case": {
        "directValues"   : ["upper", "lower"], 
        "valueSegments"  : [],
    },
    "stop script target": {
        "directValues"   : ["all", "this script", "other scripts in sprite"], 
        "valueSegments"  : [],
    },
    "stage || other sprite": {
        "directValues"   : [], 
        "valueSegments"  : ["stage", "other sprite"],
    },
    "cloning target": {
        "directValues"   : [], 
        "valueSegments"  : ["myself if not stage", "other sprite"],
        "fallback"       : ["fallback", " "],
    },
    "up|down": {
        "directValues"   : ["up", "down"], 
        "valueSegments"  : [],
    },
    "loudness|timer": {
        "directValues"   : ["loudness", "timer"], 
        "oldDirectValues": ["LOUDNESS", "TIMER"],
        "valueSegments"  : [],
    },
    "mouse || other sprite": {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "other sprite"],
    },
    "mouse|edge || other sprite": {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "edge", "other sprite"],
    },
    "mouse|edge || myself || other sprite" : {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "edge", "myself", "other sprite"],
    },
    "x|y": {
        "directValues"   : ["x", "y"], 
        "valueSegments"  : [],
    },
    "drag mode": {
        "directValues"   : ["draggable", "not draggable"], 
        "valueSegments"  : [],
    },
    "mutable sprite property": {
        "directValues"   : [], 
        "valueSegments"  : ["mutable sprite property"],
    },
    "readable sprite property": {
        "directValues"   : [], 
        "valueSegments"  : ["readable sprite property"],
    },
    "time property": {
        "directValues"   : ["year", "month", "date", "day of week", "hour", "minute", "second", "js timestamp"], 
        "oldDirectValues": ["YEAR", "MONTH", "DATE", "DAYOFWEEK"  , "HOUR", "MINUTE", "SECOND",    "TIMESTAMP"],
        "valueSegments"  : [],
    },
    "finger index": {
        "directValues"   : ["1", "2", "3", "4", "5"], 
        "valueSegments"  : [],
    },
    "random|mouse || other sprite": {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["random position", "mouse-pointer", "other sprite"],
    },
    "rotation style": {
        "directValues"   : ["left-right", "up-down", "don't rotate", "look at", "all around"], 
        "valueSegments"  : [],
    },
    "stage zone": {
        "directValues"   : ["bottom-left", "bottom", "bottom-right", "top-left", "top", "top-right", "left", "right"], 
        "valueSegments"  : [],
    },
    "text bubble color property": {
        "directValues"   : ["border"       , "fill",        "text"     ], 
        "oldDirectValues": ["BUBBLE_STROKE", "BUBBLE_FILL", "TEXT_FILL"],
        "valueSegments"  : [],
    },
    "text bubble property": {
        "directValues"   : ["MIN_WIDTH"    , "MAX_LINE_WIDTH", "STROKE_WIDTH"     , "PADDING"     , "CORNER_RADIUS", "TAIL_HEIGHT", "FONT_HEIGHT_RATIO"  , "texlim"           ], 
        "oldDirectValues": ["minimum width", "maximum width" , "border line width", "padding size", "corner radius", "tail height", "font pading percent", "text length limit"],
        "valueSegments"  : [],
    },
    "sprite effect": {
        "directValues"   : ["color", "fisheye", "whirl", "pixelate", "mosaic", "brightness", "ghost", "saturation", "red", "green", "blue", "opaque"], 
        "oldDirectValues": ["COLOR", "FISHEYE", "WHIRL", "PIXELATE", "MOSAIC", "BRIGHTNESS", "GHOST", "SATURATION", "RED", "GREEN", "BLUE", "OPAQUE"],
        "valueSegments"  : [],
    },
    "costume": {
        "directValues"   : [], 
        "valueSegments"  : ["costume"],
    },
    "backdrop": {
        "directValues"   : [], 
        "valueSegments"  : ["backdrop"],
    },
    "costume property": {
        "directValues"   : ["width", "height", "rotation center x", "rotation center y", "drawing mode"], 
        "valueSegments"  : [],
    },
    "myself || other sprite": {
        "directValues"   : [], 
        "valueSegments"  : ["myself", "other sprite"],
    },
    "front|back": {
        "directValues"   : ["front", "back"], 
        "valueSegments"  : [],
    },
    "forward|backward": {
        "directValues"   : ["forward", "backward"], 
        "valueSegments"  : [],
    },
    "infront|behind": {
        "directValues"   : ["infront", "behind"], 
        "valueSegments"  : [],
    },
    "number|name": {
        "directValues"   : ["number", "name"], 
        "valueSegments"  : [],
    },
    "sound": {
        "directValues"   : [], 
        "valueSegments"  : ["sound"],
        "fallback"       : ["fallback", " "],
    },
    "sound effect": {
        "directValues"   : ["pitch", "pan"], 
        "oldDirectValues": ["PITCH", "PAN"],
        "valueSegments"  : [],
    },
    "blockType": {
        "directValues"   : ["instruction", "lastInstruction", "textReporter", "numberReporter", "booleanReporter"], 
        "valueSegments"  : [],
    },
}

def getOptimizedOptionValuesUsingContext(optionType, context, inputDatas):
    optionTypeData = optionTypeDatabase[optionType]
    values = []
    for value in optionTypeData["directValues"]:
        if   isinstance(value, list):
            values.append(value)
        else:
            values.append(["value", value])
    for segment in optionTypeData["valueSegments"]:
        match segment:
            case "stage":
                values += [["stage", "stage"]]
            case "myself":
                values += [["myself", "myself"]]
            case "mouse-pointer":
                values += [["object", "mouse-pointer"]]
            case "random position":
                values += [["object", "random position"]]
            case "edge":
                values += [["object", "edge"]]
            
            case "myself if not stage":
                if not context["isStage"]:
                    values += [["myself", "myself"]]
            
            case "other sprite":
                values += context["otherSprites"]
            case "mutable sprite property":
                # works only for "set [PROPERTY] of ([TARGET]) to (VALUE)"; no other block uses this though
                if inputDatas["TARGET"]["option"] == "_stage_":
                    nameKey = None
                else:
                    nameKey = tuple(inputDatas["TARGET"]["option"]) # Tuples used for allowing hashing
                if nameKey == None:
                    values += [["value", "backdrop"], ["value", "volume"]]
                    values += context["globalVariables"]
                else:
                    values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume"], ["value", "size"], ["value", "volume"]]
                    values += context["localVariables"][nameKey]
            case "readable sprite property":
                # works only for "[PROPERTY] of ([TARGET])"; no other block uses this though
                if inputDatas["TARGET"]["option"] == "_stage_":
                    nameKey = None
                else:
                    nameKey = tuple(inputDatas["TARGET"]["option"]) # Tuples used for allowing hashing
                if nameKey == None:
                    values += [["value", "backdrop #"], ["value", "backdrop name"], ["value", "volume"]]
                    values += context["globalVariables"]
                else:
                    values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume #"], ["value", "costume name"], ["value", "layer"], ["value", "size"], ["value", "volume"]]
                    values += context["localVariables"][nameKey]
            case "costume":
                values += context["costumes"]
            case "backdrop":
                values += context["backdrops"]
            case "sound":
                values += context["sounds"]
    if values == [] and "fallback" in optionTypeData:
        values.append(optionTypeData["fallback"])
    return removeDuplicates(values)

def getOptimizedOptionValuesUsingNoContext(optionType):
    optionTypeData = optionTypeDatabase[optionType]
    values         = []
    defaultPrefix  = None
    for value in optionTypeData["directValues"]:
        if   isinstance(value, list):
            values.append(value)
        else:
            values.append(["value", value])
    for segment in optionTypeData["valueSegments"]:
        match segment:
            case "stage":
                values += [["stage", "stage"]]
            case "myself":
                values += [["myself", "myself"]]
            case "mouse-pointer":
                values += [["object", "mouse-pointer"]]
            case "random position":
                values += [["object", "random position"]]
            case "edge":
                values += [["object", "edge"]]
            
            case "myself if not stage":
                values += [["myself", "myself"]]
            
            case "other sprite":
                values += [["stage", "stage"]]
                defaultPrefix = "sprite"
            case "mutable sprite property":
                values += [["value", "backdrop"], ["value", "volume"]]
                values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume"], ["value", "size"]] #["value", "volume"]
                defaultPrefix = "variable"
            case "readable sprite property":
                values += [["value", "backdrop #"], ["value", "backdrop name"], ["value", "volume"]]
                values += [["value", "x position"], ["value", "y position"], ["value", "direction"], ["value", "costume #"], ["value", "costume name"], ["value", "layer"], ["value", "size"]] #["value", "volume"]
                defaultPrefix = "variable"
            case "costume":
                # Can't be guessed
                defaultPrefix = "costume"
            case "backdrop":
                # Can't be guessed
                defaultPrefix = "backdrop"
            case "sound":
                # Can't be guessed
                defaultPrefix = "sound"
    if "fallback" in optionTypeData:
        values.append(optionTypeData["fallback"])
    return removeDuplicates(values), defaultPrefix

def getDeoptimizedOptionValues(optionType):
    optionTypeData = optionTypeDatabase[optionType]
    values = []
    for value in optionTypeData["directValues"]:
        if   isinstance(value, list):
            values.append(value[0])
        else:
            values.append(value)
    for segment in optionTypeData["valueSegments"]:
        match segment:
            case "stage":
                values += ["_stage_"]
            case "myself":
                values += ["_myself_"]
            case "mouse-pointer":
                values += ["_mouse_"]
            case "random position":
                values += ["_random_"]
            case "edge":
                values += ["_edge_"]
            
            case "myself if not stage":
                values += ["_myself_"]
            
            case "other sprite":
                values += ["_stage_"]
            case "mutable sprite property":
                values += ["backdrop", "volume"]
                values += ["x position", "y position", "direction", "costume", "size"] #"volume"
            case "readable sprite property":
                values += ["backdrop #", "backdrop name", "volume"]
                values += ["x position", "y position", "direction", "costume #", "costume name", "layer", "size"] #"volume"
            case "costume":
                pass # Can't be guessed
            case "backdrop":
                pass # Can't be guessed
            case "sound":
                pass # Can't be guessed
    if "fallback" in optionTypeData:
        values.append(optionTypeData["fallback"][1])
    return removeDuplicates(values)

def optimizeOptionValue(optionValue, optionType):
    if optionType in ["broadcast", "reporter name", "opcode", "boolean"]:
        return ["value", optionValue]
    if optionType in ["variable", "list"]:
        return [optionType, optionValue]
    optimizedValues, defaultPrefix = getOptimizedOptionValuesUsingNoContext(optionType=optionType)
    deoptimizedValues              = getDeoptimizedOptionValues            (optionType=optionType)
    if len(optimizedValues) != len(deoptimizedValues):
        raise Exception()
    
    if optionValue in deoptimizedValues:
        result = optimizedValues[deoptimizedValues.index(optionValue)]
    else:
        if defaultPrefix == None: raise Exception()
        result = [defaultPrefix, optionValue]
    print("\n~", optionType, repr(optionValue))
    print("->", result)
    print("<-", repr(deoptimizeOptionValue(result, optionType)))
    return result

def deoptimizeOptionValue(optionValue, optionType):
    if optionType in ["broadcast", "reporter name", "opcode", "variable", "list", "boolean"]:
        return optionValue[1]
    optimizedValues, defaultPrefix = getOptimizedOptionValuesUsingNoContext(optionType=optionType)
    deoptimizedValues              = getDeoptimizedOptionValues            (optionType=optionType)
    if len(optimizedValues) != len(deoptimizedValues):
        raise Exception()
    
    if optionValue in optimizedValues:
        return deoptimizedValues[optimizedValues.index(optionValue)]
    else:
        return optionValue[1]


defaultCostume = {
    "name": "empty costume",
    "extension": "svg",
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
