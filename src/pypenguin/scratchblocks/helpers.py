from enum import Enum

class TokenType(Enum):
    CHARS                 = 0

    BOOLEAN_BLOCK_INPUT   = 1
    SCRIPT_INPUT          = 2
    ROUND_MENU_INPUT      = 3
    NUMBER_OR_BLOCK_INPUT = 4
    SQUARE_MENU_INPUT     = 5
    TEXT_INPUT            = 6

    TEXT_OR_BLOCK_INPUT   = 7
    
    NEWLINE               = 8

    def __repr__(self):
        return self.name

class Token:
    def __init__(self, type, value):
        self.type : TokenType  = type
        self.value             = value
    def __repr__(self):
        if   self.type == TokenType.CHARS                : abbr = "c"
        elif self.type == TokenType.BOOLEAN_BLOCK_INPUT  : abbr = "BB"
        elif self.type == TokenType.SCRIPT_INPUT         : abbr = "S"
        elif self.type == TokenType.ROUND_MENU_INPUT     : abbr = "RM"
        elif self.type == TokenType.NUMBER_OR_BLOCK_INPUT: abbr = "NB"
        elif self.type == TokenType.SQUARE_MENU_INPUT    : abbr = "SM"
        elif self.type == TokenType.TEXT_INPUT           : abbr = "T"
        elif self.type == TokenType.TEXT_OR_BLOCK_INPUT  : abbr = "TB"

        elif self.type == TokenType.NEWLINE:
            return f"{self.type.name}"
        if self.value == None:
            return abbr
        return f"{abbr}{repr(self.value)}"

class PathItemType(Enum):
    LINE_NUMBER           = 0

    BOOLEAN_BLOCK_INPUT   = 1
    SCRIPT_INPUT          = 2
    ROUND_MENU_INPUT      = 3
    NUMBER_OR_BLOCK_INPUT = 4

class PathItem:
    def __init__(self, type, value):
        self.type : PathItemType = type
        self.value               = value
    def __repr__(self):
        return f"<{self.type.name}: {repr(self.value)}>"

class ParseState(Enum):
    DEFAULT        = 0
    ANGLE_BRACKET  = 1
    CURLY_BRACKET  = 2
    ROUND_BRACKET  = 3
    SQUARE_BRACKET = 4

class Symbol(Enum):
    ANGLE_BRACKET  = 0
    CURLY_BRACKET  = 1
    ROUND_BRACKET  = 2
    SQUARE_BRACKET = 3

from pypenguin.database import opcodeDatabase
from pypenguin.helper_functions import ikv

def getAllTokenOpcodes():
    tokenOpcodes = []
    for i, oldOpcode, opcodeData in ikv(opcodeDatabase):
        newOpcode = opcodeData["newOpcode"]
        newOpcodeChars = []
        for j, char in enumerate(newOpcode):
            lastChar = newOpcode[j-1] if j-1 in range(len(newOpcode)) else None
            nextChar = newOpcode[j+1] if j+1 in range(len(newOpcode)) else None
            if   lastChar == "(" and char == "[":
                newOpcodeChars.pop()
                newOpcodeChars.append("([")
            elif lastChar == "]" and char == ")":
                newOpcodeChars.pop()
                newOpcodeChars.append("])")
            else:
                newOpcodeChars.append(char)
        
        tokens    = []
        lastIndex = 0
        for j, char in enumerate(newOpcodeChars):
            if   char == "<" : token = Token(TokenType.BOOLEAN_BLOCK_INPUT, None) 
            elif char == "{" : token = Token(TokenType.SCRIPT_INPUT       , None)
            elif char == "[" : token = Token(TokenType.SQUARE_MENU_INPUT  , None)
            elif char == "([": token = Token(TokenType.ROUND_MENU_INPUT   , None)
            elif char == "(" : token = Token(TokenType.TEXT_OR_BLOCK_INPUT, None)
            
            if   char in ["<", "{", "[", "([", "("]:
                textChars = "".join(newOpcodeChars[lastIndex:j]).strip()
                if textChars != "":
                    tokens.append(Token(TokenType.CHARS, textChars))
                tokens.append(token)
            elif char in [">", "}", "]", ")]", ")"]:
                lastIndex = j + 1
        tokenOpcodes.append((oldOpcode, tokens))
        print("-", newOpcode, tokens)
    return tokenOpcodes
