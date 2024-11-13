import random
random.seed(0)

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

def generateSelector(scriptIDs:list[int]|str, isComment:bool):
    if isinstance(scriptIDs, str):
        scriptIDs = [literalToNumber(i) for i in scriptIDs.split(":")]
    
    items = []
    for scriptID in scriptIDs:
        items.append(numberToLiteral(scriptID))
    if isComment:
        items.append("c")
    return ":".join(items)


class tempSelector:
    def __init__(self, path):
        if isinstance(path, tempSelector):
            self.path = path.path
        else:
            self.path = path

    def __eq__(self, other):
        if isinstance(other, tempSelector):
            return self.path == other.path
        return False

    def __hash__(self):
        # Use a tuple of the attributes to create a unique hash
        return hash(tuple(self.path))

    def __add__(self, other):
        if isinstance(other, list):
            return tempSelector(path=self.path+other)
        else:
            raise Exception()

    def __repr__(self):
        return f"tS<{self.path}>"
