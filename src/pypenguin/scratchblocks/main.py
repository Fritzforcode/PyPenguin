if __name__ == "__main__": import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers import *
from pypenguin.helper_functions import pp, insureCorrectPath

tokenOpcodes = getAllTokenOpcodes()

def tokenize(string: str):
    def endCharToken():
        nonlocal tokenChars
        tokenChars = tokenChars.strip()
        if tokenChars != "":
            tokens.append(Token(TokenType.CHARS, tokenChars))
            tokenChars = ""
    
    def endBracket(keepScript:bool=False):
        nonlocal bracketChars, bracketMemory, state
        if state == ParseState.DEFAULT:
            return
        if state == ParseState.CURLY_BRACKET:
            doAdd         = not keepScript
            doChangeState = not keepScript
        else:
            doAdd         = True
            doChangeState = True
        
        if doAdd:
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
        if doChangeState:
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
            (char == ">" and state == ParseState.ANGLE_BRACKET)
        or  (char == "}" and state == ParseState.CURLY_BRACKET)  
        or  (char == ")" and state == ParseState.ROUND_BRACKET)
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

    def handleNewline():
        nonlocal tokens, bracketChars
        endCharToken()
        endBracket(keepScript=True)
        if state == ParseState.CURLY_BRACKET:
            bracketChars += "\n"
        else:
            tokens.append(Token(TokenType.NEWLINE, None))

    tokens        = []
    tokenChars    = ""
    bracketChars  = ""
    bracketMemory = []
    state         = ParseState.DEFAULT
    wasEscaped    = True
    isEscaped     = False
    for char in string:

        doCloseEscaped = True
        if   char == "\\" and not isEscaped:
            isEscaped = True
            doCloseEscaped = False
        
        elif char == "\n":
            handleNewline()

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
    return tokens

def parse(string: str):
    tokens = tokenize(string)

    newTokens = []
    for token in tokens:
        token: Token
        #if   token.type in [TokenType.BOOLEAN_BLOCK_INPUT, TokenType.ROUND_MENU_INPUT, TokenType.NUMBER_OR_BLOCK_INPUT, #TokenType.SQUARE_MENU_INPUT, TokenType.TEXT_INPUT]:
        #    newTokens.append(Token(token.type, parse(token.value)[0]))
        #elif token.type == TokenType.SCRIPT_INPUT:
        #    newTokens.append(Token(token.type, parse(token.value)))
        #else:
        newTokens.append(token)

    lines = []
    lineTokens = []
    for token in tokens:
        token: Token
        if token.type == TokenType.NEWLINE:
            lines.append(lineTokens)
            lineTokens = []
        else:
            lineTokens.append(token)
    if lineTokens != []:
        lines.append(lineTokens)
    for line in lines:
        parseLine(line)
    

def parseLine(tokens: str):
    print("<", tokens)

    for opcode, opcodeTokens in tokenOpcodes:
        if len(tokens) != len(opcodeTokens):
            isSimilar = False
        else:
            isSimilar = True
            for token, opcodeToken in zip(tokens, opcodeTokens):
                token: Token
                opcodeToken: Token
                isSimilar = token.isSimilar(opcodeToken)
                if not isSimilar:
                    break
        if isSimilar:
            print("=", opcode, opcodeTokens)

string = open(insureCorrectPath("src/pypenguin/scratchblocks/code.txt", "PyPenguin")).read().strip()
pp(parse(string))
