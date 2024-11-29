import random, hashlib
random.seed(0)

literalCharSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%()*+,-./:;=?@[]^_`{|}~"
charsetLength = len(literalCharSet)

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

class newTempSelector:
    def __init__(self):
        self.id = random.randint(1, 10000)
    
    def __eq__(self, other):
        if isinstance(other, newTempSelector):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"tSn<{self.id % 1000}>"
    
    def copy(self):
        new = newTempSelector()
        new.id = self.id
        return new

def encryptStringToToken(string: str):
    hashed = hashliv.sha256(string.encode()).hexdigest()
    return 
