import os
import hashlib
from PIL import Image
import xml.etree.ElementTree as ET
from json import dump
from jsoncomment import JsonComment

# -----------------------
# File and Image Handling Functions
# -----------------------
parser = JsonComment()

def insureCorrectPath(path, targetFolderName):
    if path is None:
        return path

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
    filePath = insureCorrectPath(filePath, "PyPenguin")
    print("read", filePath)
    with open(filePath, "r", encoding="utf-8") as file:
        string = file.read()
    return parser.loads(string)

def writeJSONFile(filePath, data, beautiful: bool = True):
    filePath = insureCorrectPath(filePath, "PyPenguin")
    print("write", filePath)
    with open(filePath, "w") as file:
        if beautiful:
            dump(data, file, indent=4)
        else:
            dump(data, file)
