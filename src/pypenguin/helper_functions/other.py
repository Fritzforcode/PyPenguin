from pprint import pformat
import re, os, hashlib, difflib
from PIL import Image
from enum import Enum

def escapeChars(inputString: str, charsToEscape: list) -> str:
    # Escape backslashes first by doubling them up
    escapedString = re.sub(r'\\', r'\\\\', inputString)
    
    # Escape each character in chars_to_escape by adding a backslash before it
    for char in charsToEscape:
        escapedString = re.sub(re.escape(char), r'\\' + char, escapedString)
    
    return escapedString

def unescapeChars(inputString: str) -> str:
    # Use regex to replace any backslash followed by a character with the character itself
    return re.sub(r"\\(.)", r"\1", inputString)

def parseCustomOpcode(customOpcode: str):
    part = ""
    mode = None
    arguments = {}
    isEscaped = False
    justCompletedArgument = False
    proccode = ""
    for i, char in enumerate(customOpcode):
        if char == "\\":
            justCompletedArgument = False
            if isEscaped:
                part += "\\"
            isEscaped = not isEscaped
        elif char == "(":
            justCompletedArgument = False
            if isEscaped:
                isEscaped = False
                part += char
            else:
                mode = str
                if not part.endswith(" "):
                    part += " "
                proccode += part
                proccode += "%s "
                part = ""
        elif char == "<":
            justCompletedArgument = False
            if isEscaped:
                isEscaped = False
                part += char
            else:
                mode = bool
                if not part.endswith(" "):
                    part += " "
                proccode += part
                proccode += "%b "
                part = ""
        elif char == ")":
            if isEscaped:
                part += char
            else:
                if mode != str: raise Exception()
                arguments[part] = str
                part = ""
                justCompletedArgument = True
        elif char == ">":
            if isEscaped:
                part += char
            else:
                if mode != bool: raise Exception()
                arguments[part] = bool
                part = ""
                justCompletedArgument = True
        else:
            if char == " " and justCompletedArgument:
                pass
            else:
                justCompletedArgument
                isEscaped = False
                part += char
    proccode += part
    proccode = proccode.removesuffix(" ")
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
        if   char==" " and char2=="%" and char3=="s": # if the next chars are ' %s'
            argumentName = escapeChars(argumentNames[j], chars_to_escape)
            customOpcode += " (" + argumentName + ")"
            j += 1
            i += 2
        elif char==" " and char2=="%" and char3=="b": # if the next chars are ' %b'
            argumentName = escapeChars(argumentNames[j], chars_to_escape)
            customOpcode += " <" + argumentName + ">"
            j += 1
            i += 2
        else:
            customOpcode += escapeChars(char, chars_to_escape)
        i += 1
    return customOpcode.removesuffix(" ")

def ikv(data:dict): # Iterate through a dict with i(ndex of the pair), k(ey) and v(alue)
    return zip(
        range(len(data)),
        data.keys(),
        data.values(),
    )

def pp(*objects, sep=" ", end="\n"): # pretty print with settings i like
    string = ""
    for i, object in enumerate(objects):
        string += pformat(object, sort_dicts=False)
        if i+1 in range(len(objects)):
            string += sep
    string += end
    print(string)

def flipKeysAndValues(obj: dict):
    return dict(zip(obj.values(), obj.keys()))

def removeDuplicates(items):
    newItems = []
    [newItems.append(value) for value in items if value not in newItems]
    return newItems

def insureCorrectPath(path, targetFolderName):
    if path == None: return path
    
    initialPath = __file__
    # Normalize the path to avoid inconsistencies
    currentPath = os.path.normpath(initialPath)
    
    while True:
        # Get the last component of the path
        baseName = os.path.basename(currentPath)
        
        # Check if the current path ends with the target folder name
        if baseName == targetFolderName and os.path.isdir(currentPath):
            break
        
        # Get the parent Dir
        parentPath = os.path.dirname(currentPath)
        
        # If we've reached the root and still not found the target, stop
        if parentPath == currentPath:
            raise ValueError(f"Target folder '{targetFolderName}' not found in the path '{initialPath}'")
        
        # Update the current path to the parent
        currentPath = parentPath
    
    finalPath = os.path.join(currentPath, path)
    return finalPath

def generateMd5(file):
    """
    Generate an MD5 hash for a string or file.

    Parameters:
        data (str): The input string or file path.

    Returns:
        str: The MD5 hash as a hexadecimal string.
    """
    md5Hash = hashlib.md5()

    try:
        with open(file, "rb") as fileObj:
            for chunk in iter(lambda: fileObj.read(4096), b""):
                md5Hash.update(chunk)
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {e}"

    return md5Hash.hexdigest()

def getImageSize(file):
    _, extension = os.path.splitext(file)
    if  extension == ".svg":
        return getSVGImageSize(file=file)
    
    with Image.open(file) as image:
        size = image.size
    return size

import xml.etree.ElementTree as ET

def getSVGImageSize(file):
    # Parse the SVG file
    tree = ET.parse(file)
    root = tree.getroot()
    
    # Get width and height attributes
    width  = root.attrib.get('width')
    height = root.attrib.get('height')
    
    # If width and height are not directly specified, use viewBox
    if not width or not height:
        viewBox = root.attrib.get('viewBox')
        if viewBox:
            # Parse the viewBox attribute (min-x, min-y, width, height)
            _, _, width, height = map(float, viewBox.split())
    
    return float(width), float(height)

def getListOfClosestStrings(string, possibleValues) -> str:
    # Calculate similarity scores
    similarityScores = [(item, difflib.SequenceMatcher(None, string, item).ratio()) for item in possibleValues]
    
    # Sort by similarity score in descending order
    sortedMatches = sorted(similarityScores, key=lambda x: x[1], reverse=True)
    
    # Get the top 10 matches
    topTenMatches = [i[0] for i in sortedMatches[:10]]
    result = ""
    for match in topTenMatches:
        result += f"\n- '{match}'"
    return result


class Platform(Enum):
    PENGUINMOD = 0
    SCRATCH    = 1
