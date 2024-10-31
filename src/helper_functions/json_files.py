from json import dump
from jsoncomment import JsonComment
parser = JsonComment()

def readJSONFile(filePath):
    def read(filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            string = file.read()
        print(string)
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

def writeJSONFile(filePath, data):
    def write(filePath, data):
        with open(filePath, "w") as file:
            dump(data, file, indent=4)
    try:
        return write(filePath=filePath, data=data)
    except FileNotFoundError:
        try:
            filePath = "../" + filePath # Go up a directory
            return write(filePath=filePath, data=data)
        except FileNotFoundError:
            filePath = "../" + filePath # Go up a second directory
            return write(filePath=filePath, data=data)
