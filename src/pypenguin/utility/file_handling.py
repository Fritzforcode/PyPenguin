import os
import hashlib
import shutil
import requests
from PIL import Image
import xml.etree.ElementTree as ET
from json import dump
from jsoncomment import JsonComment
from pathlib import Path
import urllib.parse

# ------
# Errors
# ------
class PathError      (Exception): pass
class FileNotFound   (PathError): pass
class DirNotFound    (PathError): pass
class InvalidFilePath(PathError): pass
class InvalidDirPath (PathError): pass

# -----------------------
# File and Image Handling Functions
# -----------------------
parser = JsonComment()

def ensureExtension(filePath, extension): 
    base_name, _ = os.path.splitext(filePath)  # Split file name and ext
    return base_name + "." + extension  # Append/replace extension

def ensureCorrectPath(path, targetFolderName=None, ensureIsValid=False, ensureExists=False, isDir=False, allowNone=False):
    if allowNone and (path == None): return path
    
    if ensureIsValid:
        isValid = type(path) == str
        if isValid:
            if isDir:
                pathObj = Path(path)
                isValid = pathObj.is_dir() or (pathObj != '' and not pathObj.is_reserved())
            else:
                isValid = isValidFilePath(path)
        if not isValid:
            if isDir: raise InvalidDirPath ("Invalid directory path: "+repr(path))
            else    : raise InvalidFilePath("Invalid file path: "     +repr(path))
    
    if targetFolderName != None:
        initialPath = __file__
        currentPath = os.path.normpath(initialPath)

        while True:
            baseName = os.path.basename(currentPath)
            
            if baseName == targetFolderName and os.path.isdir(currentPath):
                break
            
            parentPath = os.path.dirname(currentPath)
            
            if parentPath == currentPath:
                raise PathError(f"Target folder '{targetFolderName}' not found in the path '{initialPath}'")
            
            currentPath = parentPath

        finalPath = os.path.join(currentPath, path)
        if ensureExists and not(os.path.exists(finalPath)):
            if isDir: raise DirNotFound (f"Couldn't find directory: "+repr(path))
            else    : raise FileNotFound(f"Couldn't find file: "     +repr(path))    
        return finalPath    
    
def ensureEmptyDir(directoryPath):
    # Ensure a directory exists and is empty
    # Remove the directory if it exists
    if os.path.exists(directoryPath):
        shutil.rmtree(directoryPath)  # Deletes the directory and all its contents
    
    # (Re)Create the directory
    os.makedirs(directoryPath)

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

def getUniqueFilename(baseName):
    """
    Generate a unique filename by appending a numeric suffix if needed.

    Args:
        baseName (str): Desired filename (e.g., "abc").

    Returns:
        str: A unique filename.
    """
    if not os.path.exists(baseName):
        return baseName  # If the file doesn't exist, return it directly
    
    # Extract name and extension
    name, ext = os.path.splitext(baseName)
    counter = 1

    # Generate a new filename with a numeric suffix
    while True:
        newName = f"{name}-{counter}{ext}"
        if not os.path.exists(newName):
            return newName
        counter += 1

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


def getAudioInfo(filePath):
    from mutagen.mp3 import MP3
    import scipy.io.wavfile
    from pydub import AudioSegment
    """
    Extracts the sample rate and sample count from a WAV or MP3 file.

    Parameters:
    filePath (str): Path to the audio file.

    Returns:
    tuple: (sampleRate, sampleCount)
    """
    if filePath.lower().endswith(".wav"):
        sampleRate, data = scipy.io.wavfile.read(filePath)
        sampleCount = data.shape[0]
    elif filePath.lower().endswith(".mp3"):
        audio = MP3(filePath)
        sampleRate = int(audio.info.sample_rate)
        sampleCount = int(audio.info.length * sampleRate)  # Convert duration to samples
    else:
        raise ValueError("Unsupported file format. Only WAV and MP3 are supported.")

    return sampleRate, sampleCount

def readJSONFile(filePath, ensurePath=False):
    if ensurePath:
        filePath = ensureCorrectPath(filePath, "PyPenguin")
    print("read", filePath)
    with open(filePath, "r", encoding="utf-8") as file:
        string = file.read()
    return parser.loads(string)

def writeJSONFile(filePath, data, beautiful: bool = True):
    #filePath = ensureCorrectPath(filePath, "PyPenguin")
    print("write", filePath)
    with open(filePath, "w") as file:
        if beautiful:
            dump(data, file, indent=4)
        else:
            dump(data, file)


assetLinks = None
def loadLinks():
    global assetLinks
    if assetLinks == None:
        assetLinks = readJSONFile("assets/asset_links.json", ensurePath=True)
"""
def downloadCostume(name, fileName):
    try:
        link = assetLinks["costumes"][name]
    except KeyError:
        raise ValueError(f"Unknown PenguinMod costume: {repr(name)}")
    
    cutLink   = link.removesuffix("/get/") if "/get/" in link else link
    extension = cutLink[cutLink.rindex(".")+1:]
    fileName  = ensureExtension(fileName, extension)
    #ensureCorrectPath(fileName, ensureIsValid=True, isDir=False)

    response = requests.get(link, stream=True)
    response.raise_for_status()
    with open(fileName, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print("Costume downloaded successfully as", fileName)

def downloadSound(name, fileName):
    try:
        link = assetLinks["sounds"][name]
    except KeyError:
        raise ValueError(f"Unknown PenguinMod sounds: {repr(name)}")
    
    cutLink   = link.removesuffix("/get/") if "/get/" in link else link
    extension = cutLink[cutLink.rindex(".")+1:]
    fileName  = ensureExtension(fileName, extension)
    #ensureCorrectPath(fileName, ensureIsValid=True, isDir=False)

    response = requests.get(link, stream=True)
    response.raise_for_status()
    with open(fileName, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print("Sound downloaded successfully as", fileName)

"""

def downloadCostume(name: str, projectDirectory:str, spriteName:str, spriteIsStage:bool, fileName:str, doOverwrite:bool) -> dict:
    """
    name: PenguinMod costume name e.g. "Apple"
    projectDirectory: file path of your project folder
    spriteName: name of the sprite, the costume will be added to. Not encoded. e.g. "My Sprite"
    spriteIsStage: Wether the target sprite is the stage.
    fileName: The costume will be saved under this name and will be called this in your PenguinMod Project. e.g. "apple object"
    doOverwrite: Wether the costume will be downloaded again even if the file alredy exists.

    Returns: reference to the file(dict)
    """
    loadLinks()
    try:
        link = assetLinks["costumes"][name]
    except KeyError:
        raise ValueError(f"Unknown PenguinMod costume: {repr(name)}")
    
    cutLink   = link.removesuffix("/get/") if "/get/" in link else link
    extension = cutLink[cutLink.rindex(".")+1:]
    quotedSpriteName = "stage" if spriteIsStage else ("sprite_" + urllib.parse.quote(spriteName))
    dirPath   = os.path.join(
        projectDirectory,
        quotedSpriteName,
        "costumes",
    )
    fullPath  = os.path.join(dirPath, urllib.parse.quote(fileName))
    finalPath = ensureExtension(fullPath, extension)
    
    if doOverwrite or not(os.path.exists(finalPath)):
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        response = requests.get(link, stream=True)
        response.raise_for_status()
        with open(finalPath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Costume downloaded successfully as", fileName)

def downloadSound(name: str, projectDirectory:str, spriteName:str, spriteIsStage:bool, fileName:str, doOverwrite:bool) -> dict:
    """
    name: PenguinMod sound name e.g. "Squawk"
    projectDirectory: file path of your project folder
    spriteName: name of the sprite, the sound will be added to. Not encoded. e.g. "My Sprite"
    spriteIsStage: Wether the target sprite is the stage.
    fileName: The sound will be saved under this name and will be called this in your PenguinMod Project. e.g. "squawk sound"
    doOverwrite: Wether the sound will be downloaded again even if the file alredy exists.

    Returns: reference to the file(dict)
    """
    loadLinks()
    try:
        link = assetLinks["sounds"][name]
    except KeyError:
        raise ValueError(f"Unknown PenguinMod sound: {repr(name)}")
    
    cutLink   = link.removesuffix("/get/") if "/get/" in link else link
    extension = cutLink[cutLink.rindex(".")+1:]
    quotedSpriteName = "stage" if spriteIsStage else ("sprite_" + urllib.parse.quote(spriteName))
    dirPath   = os.path.join(
        projectDirectory,
        quotedSpriteName,
        "sounds",
    )
    fullPath  = os.path.join(dirPath, urllib.parse.quote(fileName))
    finalPath = ensureExtension(fullPath, extension)
    
    if doOverwrite or not(os.path.exists(finalPath)):
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        response = requests.get(link, stream=True)
        response.raise_for_status()
        with open(finalPath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Sound downloaded successfully as", fileName)

    return {"name": fileName, "extension": extension}

