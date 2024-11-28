from pprint import pprint
import re

def escape_chars(input_string: str, chars_to_escape: list) -> str:
    # Escape backslashes first by doubling them up
    escaped_string = re.sub(r'\\', r'\\\\', input_string)
    
    # Escape each character in chars_to_escape by adding a backslash before it
    for char in chars_to_escape:
        escaped_string = re.sub(re.escape(char), r'\\' + char, escaped_string)
    
    return escaped_string

def unescape_chars(input_string: str) -> str:
    # Use regex to replace any backslash followed by a character with the character itself
    return re.sub(r"\\(.)", r"\1", input_string)

def parseCustomOpcode(customOpcode: str):
    part = ""
    mode = None
    arguments = {}
    isEscaped = False
    proccode = ""
    for i, char in enumerate(customOpcode):
        if char == "\\":
            if isEscaped:
                part += "\\"
            isEscaped = not isEscaped
        elif char == "(":
            if isEscaped:
                isEscaped = False
                part += char
            else:
                mode = str
                proccode += part
                proccode += "%s"
                part = ""
        elif char == "<":
            if isEscaped:
                isEscaped = False
                part += char
            else:
                mode = bool
                proccode += part
                proccode += "%b"
                part = ""
        elif char == ")":
            if isEscaped:
                part += char
            else:
                if mode != str: raise Exception()
                arguments[part] = str
                part = ""
        elif char == ">":
            if isEscaped:
                part += char
            else:
                if mode != bool: raise Exception()
                arguments[part] = bool
                part = ""
        else:
            isEscaped = False
            part += char
    proccode += part
    return proccode, arguments

def generateCustomOpcode(proccode: str, argumentNames: list[str]):
    customOpcode = ""
    i = 0
    j = 0
    chars_to_escape = ["(", ")", "<", ">"]
    while i in range(len(proccode)):
        char  = proccode[i]
        char2 = proccode[i + 1] if i + 1 in range(len(proccode)) else None
        char3 = proccode[i + 2] if i + 2 in range(len(proccode)) else None
        if   char==" " and char2=="%" and char3=="s": # if the next chars are ' %s '
            argumentName = escape_chars(argumentNames[j], chars_to_escape)
            customOpcode += " (" + argumentName + ")"
            j += 1
            i += 2
        elif char==" " and char2=="%" and char3=="b": # if the next chars are ' %b '
            argumentName = escape_chars(argumentNames[j], chars_to_escape)
            customOpcode += " <" + argumentName + ">"
            j += 1
            i += 2
        else:
            customOpcode += escape_chars(char, chars_to_escape)
        i += 1
    return customOpcode.removesuffix(" ")

def ikv(data:dict): # Iterate through a dict with i(ndex of the pair), k(ey) and v(alue)
    return zip(
        range(len(data)),
        data.keys(),
        data.values(),
    )

def pp(obj): # pretty print with settings i like
    pprint(obj, sort_dicts=False)

def flipKeysAndValues(obj: dict):
    return dict(zip(obj.values(), obj.keys()))

def removeStringDuplicates(array):
    return dict.fromkeys(array).keys()

def customHash(obj):
    return hash(obj) % 1000

class WhatIsGoingOnError(Exception): # Just means its likely the dev's fault 
    pass
