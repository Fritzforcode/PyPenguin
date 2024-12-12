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
        newOpcode = opcodeData["newOpcode"].replace("([", "&")
        tokenTypes = []
        for i, char in enumerate(newOpcode):
            if   char == "<": tokenType = TokenType.BOOLEAN_BLOCK_INPUT  
            elif char == "{": tokenType = TokenType.SCRIPT_INPUT         
            elif char == "[": tokenType = TokenType.SQUARE_MENU_INPUT    
            elif char == "&": tokenType = TokenType.ROUND_MENU_INPUT     
            elif char == "(": tokenType = TokenType.TEXT_INPUT           
            else:
                continue
            tokenTypes.append(tokenType)
        tokenOpcodes.append((oldOpcode, tokenTypes))
    return tokenOpcodes
