from serialization import *
import ast, pprint

UNNECESSARY_AST_ATTRS = [
    "lineno",          # Line number where the node starts
    "col_offset",      # Column offset where the node starts
    "end_lineno",      # Line number where the node ends (Python 3.8+)
    "end_col_offset",  # Column offset where the node ends (Python 3.8+)
    "type_comment",    # Inline type hints (Python 3.8+)
    "kind"             # String kind of a constant (rarely used)
]

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

    print("***", node)
    node_type = node["_type"]
    if   node_type == "Module":
        node["body"] = iterate_subnodes(node["body"])
    elif node_type == "Expr":
        node["value"] = translate_node(node["value"])
    elif node_type == "BinOp":
        node["left" ] = translate_node(node["left" ])
        node["right"] = translate_node(node["right"])

    
        """elif node_type in ["List", "Tuple", "Set"]:
            new_values = iterate_subnodes(node["elts"])
            return {
                "_type": "Constant",
                "value": make_list_tuple_set(
                    node_type.lower(), 
                    new_values,
                )
            }
        elif node_type == "Dict":
            new_keys   = iterate_subnodes(node["keys"]  )
            new_values = iterate_subnodes(node["values"])
            return {
                "_type": "Constant",
                "value": make_dict(
                    node_type.lower(),
                    new_keys,
                    new_values,
                )
            }"""
    elif node_type == "Constant":
        return {
            "_type": "Constant",
            "value": serialize(node["value"])
        }
    return node

code = """
4+3*5
"""
tree = ast.parse(code)
#print(ast.dump(tree, indent=4))
json_tree = ast_to_json(tree)
pp(json_tree)
new_tree = translate_node(json_tree)
pp(new_tree)

import json
#open("out.json", "w").write(json.dumps(new_tree))
