from serialization import *
from headers import *
import ast, pprint

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

UNNECESSARY_AST_ATTRS = [
    "lineno",          # Line number where the node starts
    "col_offset",      # Column offset where the node starts
    "end_lineno",      # Line number where the node ends (Python 3.8+)
    "end_col_offset",  # Column offset where the node ends (Python 3.8+)
    "type_comment",    # Inline type hints (Python 3.8+)
    "kind"             # String kind of a constant (rarely used)
]

variables = []

def pf(obj):
    return pprint.pformat(obj, sort_dicts=False, indent=4)

def pp(obj):
    pprint.pprint(obj, sort_dicts=False, indent=4)

def ast_to_json(node):
    if isinstance(node, ast.AST):
        fields = {
            k: ast_to_json(v)
            for k, v in ast.iter_fields(node)
            if k not in UNNECESSARY_AST_ATTRS
        }
        return {"_type": type(node).__name__, **fields}
    elif isinstance(node, list):
        return [ast_to_json(x) for x in node]
    else:
        return node

def translate_node(node):
    def iterate_subnodes(subnodes):
        new_subnodes = []
        for subnode in subnodes:
            new_subnodes.append(translate_node(subnode))
        return new_subnodes
    def generate_input_value(node, isBoolean=False):
        if node["_type"] == "Constant":
            return {"text": str(node["value"])}
        else:
            return {"block": node}

    print("***", node)
    node_type = node["_type"]
    if   node_type == "Module":
        scripts = []
        blocks = []
        for subnode in node["body"]:
            result = translate_node(subnode)
            if result["_type"] == "BLOCK":
                blocks.append(result)
            elif result["_type"] == "SCRIPT":
                scripts.append(result)

        if blocks != []:
            scripts.insert(0, {
                "_type": "SCRIPT",
                "position": [0,0],
                "blocks": blocks,
            })
        return scripts

    elif node_type == "Expr":
        value = translate_node(node["value"])
        return {
            "_type": "BLOCK",
            "opcode": "call custom block",
            "inputs": {"value": generate_input_value(value)},
            "options": {"customOpcode": ["value", "VOID (value)"]},
        }

    elif node_type == "Assign":
        targets = iterate_subnodes(node["targets"])
        if len(targets) != 1:
            raise Exception("Multi-target assigns are not supported.")
        variableId = "custom::"+targets[0]["id"]
        variables.append(variableId)
        value = translate_node(node["value"])
        return {
            "_type": "BLOCK",
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {
                "VALUE": generate_input_value(value),
            },
            "options": {"VARIABLE": ["variable", variableId]},
        }

    elif node_type == "FunctionDef":
        body = iterate_subnodes(node["body"])
        customOpcode = "custom::" + node["name"]
        posonlyargs = node["args"]["posonlyargs"]
        args        = node["args"]["args"]
        vararg      = node["args"]["vararg"]
        kwonlyargs  = node["args"]["kwonlyargs"]
        kwarg       = node["args"]["kwarg"]
        if not(
                posonlyargs == []
            and vararg      == None
            and kwonlyargs  == []
            and kwarg       == None
        ): raise Exception("Fancy arguments are not supported.")
        insuranceBlocks = []
        for arg in args:
            customOpcode += " (" + arg["arg"] + ")"
            variableId = "custom::" + arg["arg"]
            variables.append(variableId)
            insuranceBlocks.append({
                "_type": "BLOCK",
                "opcode": "set [VARIABLE] to (VALUE)",
                "inputs": {"VALUE": {"block": {
                    "_type": "BLOCK",
                    "opcode": "value of text [ARGUMENT]",
                    "options": {"ARGUMENT": ["value", arg["arg"]]},
                }}},
                "options": {"VARIABLE": ["variable", variableId]},
            })
        return {
            "_type": "SCRIPT",
            "position": [0, 500],
            "blocks": [
                {
                    "_type": "BLOCK",
                    "opcode": "define custom block",
                    "options": {
                        "noScreenRefresh": ["value", True], 
                        "blockType"      : ["value", "textReporter"], 
                        "customOpcode"   : ["value", customOpcode],
                    },
                },
                *insuranceBlocks,
                *body,
            ],
        }

    elif node_type == "If":
        condition = translate_node(node["test"])
        then      = iterate_subnodes(node["body"])
        #TODO: add 'orelse'
        return {
            "_type": "BLOCK",
            "opcode": "if <CONDITION> then {THEN}",
            "inputs": {
                "CONDITION": generate_input_value(condition, isBoolean=True),
                "THEN"     : then,
            },
        }


    elif node_type == "BinOp":
        left  = translate_node(node["left" ])
        right = translate_node(node["right"])
        match node["op"]["_type"]:
            case "Add" : opcode, leftId, rightId = "(OPERAND1) + (OPERAND2)", "OPERAND1", "OPERAND2"
            case "Mult": opcode, leftId, rightId = "(OPERAND1) * (OPERAND2)", "OPERAND1", "OPERAND2"
        return {
            "_type": "BLOCK",
            "opcode": opcode,
            "inputs": {
                leftId : generate_input_value(left ),
                rightId: generate_input_value(right),
            },
        }
    
    elif node_type == "List":
        items = iterate_subnodes(node["elts"])
        if len(items) == 0:
            return {"_type": "Constant", "value": "[]"}
        can_be_simplified = True
        for item in items:
            can_be_simplified = item["_type"] == "Constant"
            if not can_be_simplified:
                break
        if can_be_simplified:
            obj = [item["value"] for item in items]
            return {"_type": "Constant", "value": json.dumps(obj)}
        
        block  = None
        for item in items:
            block = {
                "_type": "BLOCK",
                "opcode": "in array (ARRAY) add (ITEM)",
                "inputs": {
                    "ARRAY": {"text": "[]"} if block == None else {"block": block},
                    "ITEM" : generate_input_value(item),
                },
            }
        return block

    elif node_type == "Dict":
        keys   = iterate_subnodes(node["keys"])
        values = iterate_subnodes(node["values"])
        if len(keys) == 0:
            return {"_type": "Constant", "value": "{}"}
        pairs = zip(keys, values)
        can_be_simplified = True
        for item in keys + values:
            can_be_simplified = item["_type"] == "Constant"
            if not can_be_simplified:
                break
        if can_be_simplified:
            obj = {key["value"]:value["value"] for key, value in pairs}
            return {"_type": "Constant", "value": json.dumps(obj)}

        block  = None
        for key, value in pairs:
            block = {
                "_type": "BLOCK",
                "opcode": "set (KEY) to (VALUE) in (JSON)",
                "inputs": {
                    "KEY"  : generate_input_value(key  ),
                    "VALUE": generate_input_value(value),
                    "JSON" : {"text": "{}"} if block == None else {"block": block},
                },
            }
        return block
    
    elif node_type == "Constant":
        pass
    return node


from pypenguin.helper_functions import insureCorrectPath, removeDuplicates
def updatePyFile(string):
    startLiteral = "###INSERT_START###"
    endLiteral   = "###INSERT_END###"

    filePath = insureCorrectPath("src/examples/riscv_emulator/create.py", "PyPenguin")
    with open(filePath, "r") as file:
        fileString = file.read()
    startIndex = fileString.index(startLiteral) + len(startLiteral)
    endIndex   = fileString.index(endLiteral  )# + len(endLiteral  )
    prefixPart = fileString[:startIndex]
    suffixPart = fileString[endIndex:]
    newFileString = prefixPart + "\n" + string + "\n" + suffixPart
    with open(filePath, "w") as file:
        file.write(newFileString)

code = '''
def set_register(register, value):
        """Set the value of a register."""
    #:if register in register_map:
        index = register_map[register]  # Translate to index
        if index != 0:  # x0 (zero) is read-only
            registers[index] = value
'''
tree = ast.parse(code)
#print(ast.dump(tree, indent=4))
json_tree = ast_to_json(tree)
pp(json_tree)
new_tree = translate_node(json_tree)
pp(new_tree)

updatePyFile("customScripts = " + pf(new_tree) + "\ncustomVariables = " + repr(removeDuplicates(variables)))
