from json import dump
from jsoncomment import JsonComment
parser = JsonComment()

def readJSONFile(filePath):
    print("read", filePath)
    #import inspect
    #stack = inspect.stack()
    #callers = []
    #for frame in stack[1:]:
    #    filename = frame.filename
    #    print("-", filename)
    def read(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            string = file.read()
        return parser.loads(string)
    try:
        return read(filePath)
    except FileNotFoundError:
        try:
            filePath = "../" + filePath # Go up a directory
            return read(filePath)
        except FileNotFoundError:
            filePath = "../" + filePath # Go up a second directory
            return read(filePath)    

def writeJSONFile(filePath, data, beautiful:bool=True):
    print("write", filePath)
    def write(filePath, data):
        with open(filePath, "w") as file:
            if beautiful:
                dump(data, file, indent=4)
            else:
                dump(data, file)
    try:
        return write(filePath=filePath, data=data)
    except FileNotFoundError:
        try:
            filePath = "../" + filePath # Go up a directory
            return write(filePath=filePath, data=data)
        except FileNotFoundError:
            filePath = "../" + filePath # Go up a second directory
            return write(filePath=filePath, data=data)
