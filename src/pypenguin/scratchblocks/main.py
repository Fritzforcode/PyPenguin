from pypenguin.helper_functions import pp
from enum import Enum

class TokenType(Enum):
    CHARS      = 0
    TEXT_INPUT = 1

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
    DEFAULT    = 0
    SQUARE_BRACKETS = 1

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
        
        def endTextInput():
            nonlocal textInputChars
            if textInputChars != "":
                tokens.append(Token(TokenType.TEXT_INPUT, textInputChars))
                textInputChars = ""
        
        print(repr(blockLiteral))

        tokens         = []
        tokenChars     = ""
        textInputChars = ""
        state          = ParseState.DEFAULT
        isEscaped      = False
        for char in blockLiteral:
            if   char == "\\" and not isEscaped:
                isEscaped = True
            

            elif state == ParseState.DEFAULT:
                if   char.isalnum():
                    tokenChars += char
                elif char == " ":
                    endCharToken()
                elif char == "[" and not isEscaped:
                    endCharToken()
                    state = ParseState.SQUARE_BRACKETS
                else: raise Exception(char)

            
            elif state == ParseState.SQUARE_BRACKETS:
                if   char == "]" and not isEscaped:
                    state = ParseState.DEFAULT
                    endTextInput()
                else:
                    textInputChars += char

            else: raise Exception(state)
        endCharToken()

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
scratch_code = """
when green flag clicked
say[Hello!]abc
"""

"""
move (10) steps
repeat (5) times
if <x > 10>
"""

parsed_result = parse_scratchblocks(scratch_code)
#pp(parsed_result)