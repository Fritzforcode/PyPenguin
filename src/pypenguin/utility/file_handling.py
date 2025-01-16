import os
import hashlib
from PIL import Image
import xml.etree.ElementTree as ET
from json import dump
from jsoncomment import JsonComment
from pathlib import Path

# -----------------------
# File and Image Handling Functions
# -----------------------
parser = JsonComment()

def ensureCorrectPath(path, targetFolderName, ensureExists=False, ensureDirIsValid=False, ensureFileIsValid=False, allowNone=True):
    if path is None:
        if not allowNone:
            raise FileNotFoundError(path)
        return path
    if ensureExists and not(os.path.exists(path)):
        raise FileNotFoundError(path)
    pathObj = Path(path)
    if ensureDirIsValid  and not(pathObj.is_dir() or (pathObj != '' and not pathObj.is_reserved())):
        raise NotADirectoryError(path)
    if ensureFileIsValid and not(isValidFilePath):
        raise FileNotFoundError(path)

    initialPath = __file__
    currentPath = os.path.normpath(initialPath)

    while True:
        baseName = os.path.basename(currentPath)
        
        if baseName == targetFolderName and os.path.isdir(currentPath):
            break
        
        parentPath = os.path.dirname(currentPath)
        
        if parentPath == currentPath:
            raise ValueError(f"Target folder '{targetFolderName}' not found in the path '{initialPath}'")
        
        currentPath = parentPath

    finalPath = os.path.join(currentPath, path)
    return finalPath

from pathlib import Path

def isValidFilePath(filePath):
    # Create a Path object
    path = Path(filePath)

    # Check if the path is well-formed (i.e., it's not an empty string)
    if not filePath:
        return False

    # For Windows, check if the path contains invalid characters
    if os.name == 'nt':  # Windows-specific
        invalidChars = '<>:"/\\|?*'
        if any(char in filePath for char in invalidChars):
            return False

        # Check for reserved filenames (Windows)
        reservedNames = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
                         "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
        if path.name.upper() in reservedNames:
            return False

    # Check the length of the path (for OS limitations)
    if len(filePath) > 255:
        return False

    # If the path passes all checks, it is considered valid
    return True

def generateMd5(file):
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
    if extension == ".svg":
        return getSVGImageSize(file=file)

    with Image.open(file) as image:
        size = image.size
    return size

def getSVGImageSize(file):
    tree = ET.parse(file)
    root = tree.getroot()
    width = root.attrib.get('width')
    height = root.attrib.get('height')

    if not width or not height:
        viewBox = root.attrib.get('viewBox')
        if viewBox:
            _, _, width, height = map(float, viewBox.split())

    return float(width), float(height)

def readJSONFile(filePath):
    filePath = ensureCorrectPath(filePath, "PyPenguin")
    print("read", filePath)
    with open(filePath, "r", encoding="utf-8") as file:
        string = file.read()
    return parser.loads(string)

def writeJSONFile(filePath, data, beautiful: bool = True):
    filePath = ensureCorrectPath(filePath, "PyPenguin")
    print("write", filePath)
    with open(filePath, "w") as file:
        if beautiful:
            dump(data, file, indent=4)
        else:
            dump(data, file)
