optionTypeDatabase = {
    "key"                                  : {
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
    "unary math operation"                 : {
        "directValues"   : ["abs", "floor", "ceiling", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "ln", "log", "e ^", "10 ^"], 
        "valueSegments"  : [],
    },
    "power|root|log"                       : {
        "directValues"   : ["^", "root", "log"], 
        "valueSegments"  : [],
    },
    "root|log"                             : {
        "directValues"   : ["root", "log"], 
        "valueSegments"  : [],
    },
    "text method"                          : {
        "directValues"   : ["starts", "ends"], 
        "valueSegments"  : [],
    },
    "text case"                            : {
        "directValues"   : ["upper", "lower"], 
        "valueSegments"  : [],
    },
    "stop script target"                   : {
        "directValues"   : ["all", "this script", "other scripts in sprite"], 
        "valueSegments"  : [],
    },
    "stage || other sprite"                : {
        "directValues"   : [], 
        "valueSegments"  : ["stage", "other sprite"],
    },
    "cloning target"                       : {
        "directValues"   : [], 
        "valueSegments"  : ["myself if not stage", "other sprite"],
        "fallback"       : ["fallback", " "],
    },
    "up|down"                              : {
        "directValues"   : ["up", "down"], 
        "valueSegments"  : [],
    },
    "loudness|timer"                       : {
        "directValues"   : ["loudness", "timer"], 
        "oldDirectValues": ["LOUDNESS", "TIMER"],
        "valueSegments"  : [],
    },
    "mouse || other sprite"                : {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "other sprite"],
    },
    "mouse|edge || other sprite"           : {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "edge", "other sprite"],
    },
    "mouse|edge || myself || other sprite" : {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["mouse-pointer", "edge", "myself", "other sprite"],
    },
    "x|y"                                  : {
        "directValues"   : ["x", "y"], 
        "valueSegments"  : [],
    },
    "drag mode"                            : {
        "directValues"   : ["draggable", "not draggable"], 
        "valueSegments"  : [],
    },
    "mutable sprite property"              : {
        "directValues"   : [], 
        "valueSegments"  : ["mutable sprite property"],
    },
    "readable sprite property"             : {
        "directValues"   : [], 
        "valueSegments"  : ["readable sprite property"],
    },
    "time property"                        : {
        "directValues"   : ["year", "month", "date", "day of week", "hour", "minute", "second", "js timestamp"], 
        "oldDirectValues": ["YEAR", "MONTH", "DATE", "DAYOFWEEK"  , "HOUR", "MINUTE", "SECOND",    "TIMESTAMP"],
        "valueSegments"  : [],
    },
    "finger index"                         : {
        "directValues"   : ["1", "2", "3", "4", "5"], 
        "valueSegments"  : [],
    },
    "random|mouse || other sprite"         : {
        "directValues"   : [], 
        "oldDirectValues": [],
        "valueSegments"  : ["random position", "mouse-pointer", "other sprite"],
    },
    "rotation style"                       : {
        "directValues"   : ["left-right", "up-down", "don't rotate", "look at", "all around"], 
        "valueSegments"  : [],
    },
    "stage zone"                           : {
        "directValues"   : ["bottom-left", "bottom", "bottom-right", "top-left", "top", "top-right", "left", "right"], 
        "valueSegments"  : [],
    },
    "text bubble color property"           : {
        "directValues"   : ["border"       , "fill",        "text"     ], 
        "oldDirectValues": ["BUBBLE_STROKE", "BUBBLE_FILL", "TEXT_FILL"],
        "valueSegments"  : [],
    },
    "text bubble property"                 : {
        "directValues"   : ["MIN_WIDTH"    , "MAX_LINE_WIDTH", "STROKE_WIDTH"     , "PADDING"     , "CORNER_RADIUS", "TAIL_HEIGHT", "FONT_HEIGHT_RATIO"  , "texlim"           ], 
        "oldDirectValues": ["minimum width", "maximum width" , "border line width", "padding size", "corner radius", "tail height", "font pading percent", "text length limit"],
        "valueSegments"  : [],
    },
    "sprite effect"                        : {
        "directValues"   : ["color", "fisheye", "whirl", "pixelate", "mosaic", "brightness", "ghost", "saturation", "red", "green", "blue", "opaque"], 
        "oldDirectValues": ["COLOR", "FISHEYE", "WHIRL", "PIXELATE", "MOSAIC", "BRIGHTNESS", "GHOST", "SATURATION", "RED", "GREEN", "BLUE", "OPAQUE"],
        "valueSegments"  : [],
    },
    "costume"                              : {
        "directValues"   : [], 
        "valueSegments"  : ["costume"],
    },
    "backdrop"                             : {
        "directValues"   : [], 
        "valueSegments"  : ["backdrop"],
    },
    "costume property"                     : {
        "directValues"   : ["width", "height", "rotation center x", "rotation center y", "drawing mode"], 
        "valueSegments"  : [],
    },
    "myself || other sprite"               : {
        "directValues"   : [], 
        "valueSegments"  : ["myself", "other sprite"],
    },
    "front|back"                           : {
        "directValues"   : ["front", "back"], 
        "valueSegments"  : [],
    },
    "forward|backward"                     : {
        "directValues"   : ["forward", "backward"], 
        "valueSegments"  : [],
    },
    "infront|behind"                       : {
        "directValues"   : ["infront", "behind"], 
        "valueSegments"  : [],
    },
    "number|name"                          : {
        "directValues"   : ["number", "name"], 
        "valueSegments"  : [],
    },
    "sound"                                : {
        "directValues"   : [], 
        "valueSegments"  : ["sound"],
    },
    "sound effect"                         : {
        "directValues"   : ["pitch", "pan"], 
        "oldDirectValues": ["PITCH", "PAN"],
        "valueSegments"  : [],
    },
    "blockType"                            : {
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
    return removeDuplicates(values)

def optimizeOptionValue(optionValue, optionType):
    optimizedValues, defaultPrefix = getOptimizedOptionValuesUsingNoContext(optionType=optionType)
    deoptimizedValues              = getDeoptimizedOptionValues            (optionType=optionType)
    if len(optimizedValues) != len(deoptimizedValues):
        raise Exception()
    
    if optionValue in deoptimizedValues:
        return optimizedValues[deoptimizedValues.index(optionValue)]
    else:
        if defaultPrefix == None: raise Exception()
        return [defaultPrefix, optionValue]

