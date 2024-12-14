if __name__ == "__main__": import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers import *
from pypenguin.helper_functions import pp, insureCorrectPath
from pypenguin.database import getInputModes, getOptionTypes, getOptimizedOpcode

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
            if   char == "<" and not isEscaped:
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
            else:
                tokenChars += char


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

def parse(string: str, returnScript:bool=True):
    tokens = tokenize(string)
    print("&", tokens)
    newTokens = []
    for token in tokens:
        token: Token
        if   token.type in [TokenType.BOOLEAN_BLOCK_INPUT, TokenType.ROUND_MENU_INPUT]:
            block = parse(token.value, returnScript=False)[0]
            newToken = Token(TokenType.INPUT_BLOCK, block)
        elif token.type == TokenType.TEXT_INPUT:
            newToken = Token(TokenType.INPUT_LITERAL, token.value)
        elif token.type == TokenType.NUMBER_OR_BLOCK_INPUT:
            if isValidNumber(token.value):
                newToken = Token(TokenType.INPUT_LITERAL, token.value)
            else:
                block = parse(token.value, returnScript=False)[0]
                newToken = Token(TokenType.INPUT_BLOCK, block)
        elif token.type == TokenType.SCRIPT_INPUT:
            blocks = parse(token.value, returnScript=False)
            newToken = Token(TokenType.INPUT_BLOCKS, blocks)
        elif token.type == TokenType.SQUARE_MENU_INPUT:
            newToken = Token(TokenType.OPTION_LITERAL, token.value)
        elif token.type in [TokenType.CHARS, TokenType.NEWLINE]:
            newToken = token
        newTokens.append(newToken)

    lines = []
    lineTokens = []
    for token in newTokens:
        token: Token
        if token.type == TokenType.NEWLINE:
            lines.append(lineTokens)
            lineTokens = []
        else:
            lineTokens.append(token)
    if lineTokens != []:
        lines.append(lineTokens)
    
    pp(lines)
    blocks = []
    for line in lines:
        blocks.append(parseBlock(line))
    if returnScript:
        result = {
            "position": [0, 0], # placeholder
            "blocks"  : blocks,
        }
    else:
        result = blocks
    print(100*"=")
    pp(result)
    return result

def parseBlock(tokens: list[Token]):
    print("<", tokens)

    matches = []
    for opcode, opcodeTokens in tokenOpcodes:
        if len(tokens) != len(opcodeTokens):
            isSimilar = False
        else:
            isSimilar  = True
            for token, opcodeToken in zip(tokens, opcodeTokens):
                token: Token
                opcodeToken: Token
                isSimilar  = token.isSimilar2(opcodeToken)
                if not isSimilar:
                    break
        if isSimilar:
            matches.append(opcode)
    if len(matches) == 0:
        return {
            "opcode" : getOptimizedOpcode(opcode="special_variable_value"),
            "inputs" : {},
            "options": {"VARIABLE": tokens[0].value},
        }
    if len(matches) != 1:
        pp(matches)
        raise Exception()
    opcode      = matches[0]
    newOpcode   = getOptimizedOpcode(opcode=opcode)
    inputModes  = getInputModes(opcode=opcode)
    inputIDs    = list(inputModes.keys())
    optionTypes = getOptionTypes(opcode=opcode)
    optionIDs   = list(optionTypes.keys())
    print("=>", newOpcode, inputModes, optionTypes)
    
    inputs      = {}
    options     = {}
    inputIndex  = 0
    optionIndex = 0    
    for token in tokens:
        token: Token
        if   token.isInput():
            inputID = inputIDs[inputIndex]
            inputMode = inputModes[inputID]
            inputIndex += 1
            
            if inputMode == "block-and-text":
                if   token.type == TokenType.INPUT_LITERAL:
                    block = None
                    text = token.value
                elif token.type == TokenType.INPUT_BLOCK:
                    block = token.value
                    text = ""
                inputValue = {
                    "block": block,
                    "text" : text,
                }
            
            print(".", inputID, inputMode, token, inputValue)
            inputs[inputID] = inputValue
        
        elif token.type == TokenType.OPTION_LITERAL:
            optionID = optionIDs[optionIndex]
            #optionType = opionTypes[optionID] # has no effect currently
            optionIndex += 1
            
            optionValue = token.value
            options[optionID] = optionValue
    block = {
        "opcode" : newOpcode,
        "inputs" : inputs,
        "options": options,
    }
    pp(">>>", block)
    return block

string = open(insureCorrectPath("src/pypenguin/scratchblocks/code.txt", "PyPenguin")).read().strip()
pp(parse(string))
