from pprint import pprint
from json import dump
from jsoncomment import JsonComment
parser = JsonComment()
import random
random.seed(0)

def ikv(data:dict):
    return zip(
        range(len(data)),
        data.keys(),
        data.values(),
    )

def pp(obj):
    pprint(obj, sort_dicts=False)

def flipKeysAndValues(obj: dict):
    return {v:k for i,k,v in ikv(obj)}



def readJSONFile(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        string = file.read()
    return parser.loads(string)

def writeJSONFile(file_path, data):
    with open(file_path, "w") as file:
        dump(data, file, indent=4)




class WhatIsGoingOnError(Exception):
    pass





"5I9nI;7P)jdiR-_X;/%l"

literalCharSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%()*+,-./:;=?@[]^_`{|}~"

def generateRandomToken():
    #return f"Token::{random.randint(0,1000)}"
    Token = ""
    for _ in range(20):
        Token += literalCharSet[random.randrange(0, len(literalCharSet)-1)]
    return Token

def literalToNumber(literal):
    base = len(literalCharSet)
    num = 0
    for i, char in enumerate(reversed(literal)):
        num += (literalCharSet.index(char) + 1) * (base ** i)
    return num

def numberToLiteral(number):
    base = len(literalCharSet)
    result = []
    while number > 0:
        number -= 1
        result.append(literalCharSet[number % base])
        number //= base
    return ''.join(reversed(result))

def generateNextKeyInDict(obj:dict, offset=0):
    keys = list(obj.keys())
    ints = [literalToNumber(i) for i in keys]
    biggest = max([0] + ints)
    return numberToLiteral(biggest + 1 + offset)

def generateSelector(scriptID:int, index:int, isComment:bool):
    if isinstance(scriptID, int):
        return numberToLiteral(scriptID+1) + ":" + numberToLiteral(index+1) + "#" + ("c" if isComment else "b")
    elif scriptID == None:
        return numberToLiteral(index+1) + "#" + ("c" if isComment else "b")
    else: raise Exception()
