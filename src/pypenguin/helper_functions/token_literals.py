import random, hashlib
random.seed(0)

literalCharSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%()*+,-./:;=?@[]^_`{|}~"
charsetLength = len(literalCharSet)

class localStringToToken:
    def __init__(self, main: str, spriteName=None):
        self.main = main
        self.spriteName = spriteName
    def toToken(self):
        return stringToToken(main=self.main, spriteName=self.spriteName)
    def toJSON(self):
        return {"_custom_": True, "_type_": "localStringToToken", "main": self.main}

def stringToToken(main: str, spriteName=None) -> str:
    def convert(inputString: str, digits: int) -> str:
        # Character set to use in the output
        
        # Compute SHA-256 hash of the input string
        hashObject = hashlib.sha256(inputString.encode())
        hexHash = hashObject.hexdigest()
        
        # Convert the hexadecimal hash to a deterministic 20-character string
        result = []
        for i in range(digits):
            # Take 2 characters from the hash at a time and convert to an integer
            chunk = hexHash[i * 2:(i * 2) + 2]
            index = int(chunk, 16) % charsetLength
            result.append(literalCharSet[index])
        
        return ''.join(result)
    
    if spriteName == None:
        return convert(main, digits=20)
    else:
        return convert(spriteName, digits=4) + convert(main, digits=16)

def generateRandomToken():
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

class newTempSelector:
    count = 0
    def __init__(self):
        self.id = newTempSelector.count
        newTempSelector.count += 1
    def __eq__(self, other):
        if isinstance(other, newTempSelector):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"tSn::{self.id}"
    
    def copy(self):
        new = newTempSelector()
        new.id = self.id
        return new

def getSelectors(obj):
    selectors = []
    if isinstance(obj, dict):
        for k,v in obj.items():
            if isinstance(k, newTempSelector):
                selectors.append(k)
            if isinstance(v, newTempSelector):
                selectors.append(v)
            else:
                selectors += getSelectors(v)
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, newTempSelector):
                selectors.append(v)
            else:
                selectors += getSelectors(v)
    return selectors

def replaceClasses(obj, classes:list[type], convertionFunc:callable):
    if isinstance(obj, dict):
        newObj = {}
        for key, value in obj.items():
            if type(key  ) in classes: newKey = convertionFunc(key)
            else                     : newKey = replaceClasses(key, classes=classes, convertionFunc=convertionFunc)

            if type(value) in classes: newValue = convertionFunc(value)
            else                     : newValue = replaceClasses(value, classes=classes, convertionFunc=convertionFunc)
            
            newObj[newKey] = newValue
        return newObj
    if isinstance(obj, (list, tuple, set)):
        newObj = type(obj)() # Creates a new object of the same type as the old object
        for item in obj:
            if type(item) in classes: newItem = convertionFunc(item)
            else                    : newItem = replaceClasses(item, classes=classes, convertionFunc=convertionFunc)

            newObj.append(newItem)
        return newObj
    return obj # Otherwise just return the old object
