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
    
    INPUT_LITERAL         = 8
    INPUT_BLOCK           = 9
    INPUT_BLOCKS          = 10
    OPTION_LITERAL        = 11
    
    NEWLINE               = 12

    def __repr__(self):
        return self.name
    def __eq__(self, other):
        if not isinstance(other, TokenType):
            return False
        return self.value == other.value

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
        
        elif self.type == TokenType.INPUT_LITERAL        : abbr = "IL"
        elif self.type == TokenType.INPUT_BLOCK          : abbr = "IB"
        elif self.type == TokenType.INPUT_BLOCKS         : abbr = "IBs"
        elif self.type == TokenType.OPTION_LITERAL       : abbr = "OL"

        elif self.type == TokenType.NEWLINE:
            return f"{self.type.name}"
        if self.value == None:
            return abbr
        return f"{abbr}:{repr(self.value)}"
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type) and (self.value == other.value)
    def isSimilar(self, other: "Token"):
        if self.type == TokenType.CHARS:
            return self == other
        types = [self.type, other.type]
        if (TokenType.TEXT_OR_BLOCK_INPUT in types) and ((TokenType.TEXT_INPUT in types) or (TokenType.NUMBER_OR_BLOCK_INPUT in types)):
            return True
        return self.type == other.type
    def isSimilar2(self, other: "Token"):
        if self.type == TokenType.CHARS:
            return self == other
        if self.isInput() and other.isInput():
            return True
        types = []
        if (TokenType.OPTION_LITERAL in types) and ((TokenType.ROUND_MENU_INPUT in types) or (TokenType.SQUARE_MENU_INPUT in types)):
            return True
        return self.type == other.type
    def isInput(self):
        if self.type in [TokenType.BOOLEAN_BLOCK_INPUT,  TokenType.SCRIPT_INPUT, TokenType.ROUND_MENU_INPUT, TokenType.NUMBER_OR_BLOCK_INPUT, TokenType.TEXT_INPUT, TokenType.TEXT_OR_BLOCK_INPUT, TokenType.INPUT_LITERAL, TokenType.INPUT_BLOCK, TokenType.INPUT_BLOCKS]:
            return True
        return False

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

print(Token(TokenType.OPTION_LITERAL, "jhi").isSimilar2(Token(TokenType.ROUND_MENU_INPUT, None)))

from pypenguin.database import opcodeDatabase, getPredefinedTokens
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
        
        predefinedTokens = getPredefinedTokens(opcode=oldOpcode)
        tokens           = []
        if predefinedTokens == None:
            lastIndex = 0
            for j, char in enumerate(newOpcodeChars):
                if   char == "<" : token = Token(TokenType.BOOLEAN_BLOCK_INPUT, None) 
                elif char == "{" : token = Token(TokenType.SCRIPT_INPUT       , None)
                elif char == "[" : token = Token(TokenType.OPTION_LITERAL     , None)
                elif char == "([": token = Token(TokenType.ROUND_MENU_INPUT   , None)
                elif char == "(" : token = Token(TokenType.TEXT_OR_BLOCK_INPUT, None)
                
                if   char in ["<", "{", "[", "([", "("]:
                    textChars = "".join(newOpcodeChars[lastIndex:j]).strip()
                    if textChars != "":
                        tokens.append(Token(TokenType.CHARS, textChars))
                    tokens.append(token)
                elif char in [">", "}", "]", "])", ")"]:
                    lastIndex = j + 1
            textChars = "".join(newOpcodeChars[lastIndex:]).strip()
            if textChars != "":
                tokens.append(Token(TokenType.CHARS, textChars))
        else:
            for token in predefinedTokens:
                token: str
                if token.startswith('"') and token.endswith('"'):
                    tokens.append(Token(TokenType.CHARS, token.removeprefix('"').removesuffix('"')))
                else:
                    tokens.append(Token(TokenType[token], None))

        print("-", newOpcode, tokens)
        tokenOpcodes.append((oldOpcode, tokens))
    return tokenOpcodes

def isValidNumber(string: str):
    isValid = True
    for char in string:
        if char not in "01233456789.-":
            isValid = False
            break
    return isValid
