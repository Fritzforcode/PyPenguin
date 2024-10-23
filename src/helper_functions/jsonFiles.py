from json import dump
from jsoncomment import JsonComment
parser = JsonComment()

def readJSONFile(filePath):
    with open(filePath, "r", encoding="utf-8") as file:
        string = file.read()
    return parser.loads(string)

def writeJSONFile(filePath, data):
    with open(filePath, "w") as file:
        dump(data, file, indent=4)
