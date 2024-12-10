from pypenguin.helper_functions import pp, insureCorrectPath
from enum import Enum

class TokenType(Enum):
    CHARS                 = 0

    BOOLEAN_BLOCK_INPUT   = 1
    SCRIPT_INPUT          = 2
    ROUND_MENU_INPUT      = 3
    NUMBER_OR_BLOCK_INPUT = 4
    SQUARE_MENU_INPUT     = 5
    TEXT_INPUT            = 6

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
            nonlocal bracketChars, bracketMemory, state
            if bracketChars != "":
                isMenu = bracketChars.endswith(" v") and not wasEscaped
                if   isMenu:
                    bracketChars = bracketChars.removesuffix(" v")
                if   state == ParseState.ANGLE_BRACKET:
                    tokenType = TokenType.BOOLEAN_BLOCK_INPUT
                elif state == ParseState.CURLY_BRACKET:
                    tokenType = TokenType.SCRIPT_INPUT
                elif state == ParseState.ROUND_BRACKET:
                    if isMenu: tokenType = TokenType.ROUND_MENU_INPUT
                    else:      tokenType = TokenType.NUMBER_OR_BLOCK_INPUT
                elif state == ParseState.SQUARE_BRACKET:
                    if isMenu: tokenType = TokenType.SQUARE_MENU_INPUT
                    else:      tokenType = TokenType.TEXT_INPUT
                tokens.append(Token(tokenType, bracketChars))
                bracketChars = ""
                bracketMemory = []
            state = ParseState.DEFAULT
        
        def handleBracketChar():
            nonlocal bracketChars
            if not isEscaped:
                if   char == "<":
                    bracketMemory.append(Symbol.ANGLE_BRACKET)
                elif char == "(":
                    bracketMemory.append(Symbol.ROUND_BRACKET)
                elif char == "{":
                    bracketMemory.append(Symbol.CURLY_BRACKET)
                
                wasShortend = False
                if   bracketMemory != []:
                    if ((char == ">" and bracketMemory[-1] == Symbol.ANGLE_BRACKET )
                    or  (char == "}" and bracketMemory[-1] == Symbol.CURLY_BRACKET )
                    or  (char == ")" and bracketMemory[-1] == Symbol.ROUND_BRACKET )):
                        bracketMemory.pop()
                        wasShortend = True
                
            
            if  bracketMemory == [] and not(isEscaped) and not(wasShortend) and (
               (char == ">" and state == ParseState.ANGLE_BRACKET )
            or (char == "}" and state == ParseState.CURLY_BRACKET )  
            or (char == ")" and state == ParseState.ROUND_BRACKET )        
            ):
                endBracket()
                #...
            else:
                bracketChars += char
        
        def handleSquareBracketChar():
            nonlocal bracketChars
            if   char == "]" and not isEscaped:
                endBracket()
            else:
                bracketChars += char

        print(100*"{")
        print(repr(blockLiteral))

        tokens        = []
        tokenChars    = ""
        bracketChars  = ""
        bracketMemory = []
        state         = ParseState.DEFAULT
        wasEscaped    = True
        isEscaped     = False
        for char in blockLiteral:
            print(repr(char), state, bracketMemory)

            doCloseEscaped = True
            if   char == "\\" and not isEscaped:
                isEscaped = True
                doCloseEscaped = False
            

            elif state == ParseState.DEFAULT:
                if   char.isalnum() or char in [" ", ">", "}", ")", "]", "."]:
                    tokenChars += char
                elif char == "<" and not isEscaped:
                    endCharToken()
                    state = ParseState.ANGLE_BRACKET
                elif char == "{" and not isEscaped:
                    endCharToken()
                    state = ParseState.CURLY_BRACKET
                elif char == "(" and not isEscaped:
                    endCharToken()
                    state = ParseState.ROUND_BRACKET
                elif char == "[" and not isEscaped:
                    endCharToken()
                    state = ParseState.SQUARE_BRACKET
                else: raise Exception(char)


            elif state == ParseState.ANGLE_BRACKET:
                handleBracketChar()
            elif state == ParseState.CURLY_BRACKET:
                handleBracketChar()
            elif state == ParseState.ROUND_BRACKET:
                handleBracketChar()
            elif state == ParseState.SQUARE_BRACKET:
                handleSquareBracketChar()
                    

            else: raise Exception(state)
            
            wasEscaped = isEscaped
            if doCloseEscaped:
                isEscaped = False 
        endCharToken()
        endBracket()

        print("->", tokens)
        nestedTokens = []
        for token in tokens:
            token: Token
            if   token.type == TokenType.BOOLEAN_BLOCK_INPUT  : pathItemType = PathItemType.BOOLEAN_BLOCK_INPUT  
            elif token.type == TokenType.SCRIPT_INPUT         : pathItemType = PathItemType.SCRIPT_INPUT         
            elif token.type == TokenType.ROUND_MENU_INPUT     : pathItemType = PathItemType.ROUND_MENU_INPUT     
            elif token.type == TokenType.NUMBER_OR_BLOCK_INPUT: pathItemType = PathItemType.NUMBER_OR_BLOCK_INPUT 
            else: # non input types:  SQUARE_MENU_INPUT, TEXT_INPUT, CHARS
                nestedTokens.append(token)
                continue
            
            pathItem = PathItem(pathItemType, None)
            nestedTokens.append(Token(token.type, parseBlock(
                blockLiteral=token.value,
                path=path+[pathItem]
            )))

        pp(nestedTokens)
        print(110*"}")
        return nestedTokens

        
    
    # Process each line and parse it
    for i, line in enumerate(lines):
        path   = [PathItem(PathItemType.LINE_NUMBER, i)]
        parsed_data.append(
            parseBlock(
                blockLiteral=line.strip(),
                path=path,
            )
        )
    
    return parsed_data

# Example Scratchblocks code
scratch_code = open(insureCorrectPath("src/pypenguin/scratchblocks/code.txt", "PyPenguin")).read()
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