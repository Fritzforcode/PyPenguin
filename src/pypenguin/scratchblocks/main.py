from pypenguin.helper_functions import pp
from enum import Enum

class TokenType(Enum):
    CHARS                 = 0
    SQUARE_MENU_INPUT     = 1
    TEXT_INPUT            = 2
    ROUND_MENU_INPUT      = 3
    NUMBER_OR_BLOCK_INPUT = 4

class Token:
    def __init__(self, type, value):
        self.type : TokenType  = type
        self.value             = value
    def __repr__(self):
        return f"<{self.type.name}: {repr(self.value)}>"

class PathItemType(Enum):
    LINE = 0

class PathItem:
    def __init__(self, type, value):
        self.type : PathItemType = type
        self.value               = value
    def __repr__(self):
        return f"<{self.type.name}: {repr(self.value)}>"

class ParseState(Enum):
    DEFAULT         = 0
    SQUARE_BRACKETS = 1
    ROUND_BRACKETS  = 2

startWords = {
    "when"  : ["when green flag clicked"],
    "say"   : ["say ()", "say () for () secs"],
    "move"  : ["move () steps"],
    "repeat": ["repeat ()"],
    "if"    : ["if <>"],
}

def parse_scratchblocks(scratch_code):
    # Split the input code into lines
    lines = scratch_code.strip().split("\n")
    
    # This will hold the final structured output
    parsed_data = []

    # Function to parse a single line into a generic block
    def parseBlock(blockLiteral:str, path:list):
        def endCharToken():
            nonlocal tokenChars
            if tokenChars != "":
                tokens.append(Token(TokenType.CHARS, tokenChars))
                tokenChars = ""
        
        def endBracket():
            nonlocal bracketChars
            nonlocal state
            if bracketChars == "":
                return
            isMenu = bracketChars.endswith(" v") and not wasEscaped
            if   isMenu:
                bracketChars = bracketChars.removesuffix(" v")
            if   state == ParseState.SQUARE_BRACKETS:
                if isMenu:
                    tokenType = TokenType.SQUARE_MENU_INPUT
                else:                
                    tokenType = TokenType.TEXT_INPUT
            elif state == ParseState.ROUND_BRACKETS:
                if isMenu:
                    tokenType = TokenType.ROUND_MENU_INPUT
                else:
                    tokenType = TokenType.NUMBER_OR_BLOCK_INPUT
            tokens.append(Token(tokenType, bracketChars))
            bracketChars = ""
            state = ParseState.DEFAULT
        
        print(repr(blockLiteral))

        tokens       = []
        tokenChars   = ""
        bracketChars = ""
        state        = ParseState.DEFAULT
        wasEscaped   = True
        isEscaped    = False
        for char in blockLiteral:
            doCloseEscaped = True
            if   char == "\\" and not isEscaped:
                isEscaped = True
                doCloseEscaped = False
            

            elif state == ParseState.DEFAULT:
                if   char.isalnum() or char == " ":
                    tokenChars += char
                elif char == "[" and not isEscaped:
                    endCharToken()
                    state = ParseState.SQUARE_BRACKETS
                elif char == "(" and not isEscaped:
                	endCharToken()
                	state = ParseState.ROUND_BRACKETS
                else: raise Exception(char)

            
            elif state == ParseState.SQUARE_BRACKETS:
                if   char == "]" and not isEscaped:
                    endBracket()
                else:
                    bracketChars += char
                    
            elif state == ParseState.ROUND_BRACKETS:
                if   char == ")" and not isEscaped:
                    endBracket()
                else:
                    bracketChars += char

            else: raise Exception(state)
        
            
            wasEscaped = isEscaped
            if doCloseEscaped:
                isEscaped = False 
        endCharToken()
        endBracket()

        print(tokens)

        
    
    # Process each line and parse it
    for i, line in enumerate(lines):
        path   = [PathItem(PathItemType.LINE, i)]
        parsed_data.append(
            parseBlock(
                blockLiteral=line.strip(),
                path=path,
            )
        )
    
    return parsed_data

# Example Scratchblocks code
scratch_code = open("pypenguin/scratchblocks/code.txt").read()
"""
when green flag clicked
say[Hello!]abc
say[Hello! v]def
say[Hello! \\v]ghi
say[Hello! \\\\v]jkl

"""

"""
move (10) steps
repeat (5) times
if <x > 10>
"""

parsed_result = parse_scratchblocks(scratch_code)
#pp(parsed_result)