import platform
from json import dump
from jsoncomment import JsonComment
parser = JsonComment()
from pypenguin.helper_functions.other import insureCorrectPath

def readJSONFile(filePath):
    filePath = insureCorrectPath(filePath, "PyPenguin")
    print("read", filePath)
    #import inspect
    #stack = inspect.stack()
    #callers = []
    #for frame in stack[1:]:
    #    filename = frame.filename
    #    print("-", filename)
    with open(filePath, "r", encoding="utf-8") as file:
        string = file.read()
    return parser.loads(string) 

def writeJSONFile(filePath, data, beautiful:bool=True):
    filePath = insureCorrectPath(filePath, "PyPenguin")
    print("write", filePath)
    with open(filePath, "w") as file:
        if beautiful:
            dump(data, file, indent=4)
        else:
            dump(data, file)
