import json
cat = "pm_Bitwise"
string = ""
for opcode, data in opcodes.items():
    blockId = cat + "." + "_".join(opcode.split("_")[1:])
    bt = data["type"]
    if bt == "stringReporter": shape = "reporter"
    elif bt == "booleanReporter": shape = "boolean"
    elif bt == "instruction": shape = "stack"
    
    inputs = []
    spec = data["newOpcode"].replace("([", "(").replace("])", ")")
    for i, id in enumerate(list(data["inputTypes"].keys())+list(data["optionTypes"].keys())):
        a = "(" + id + ")"
        b = "<" + id + ">"
        c = "[" + id + "]"
        if a in spec:
            spec = spec.replace(a, "%"+str(i))
            inputs.append("%n")
        if b in spec:
            spec = spec.replace(b, "%"+str(i))
            inputs.append("%b")
        if c in spec:
            spec = spec.replace(c, "%"+str(i))
            inputs.append("%m")
    
    
    string += "  {\n"
    string += "    id: " + json.dumps(blockId) + "\n"
    string += "    spec: " + json.dumps(spec) + "\n"
    string += "    inputs: " + json.dumps(inputs) + "\n"
    string += "    shape: " + json.dumps(shape) + "\n"
    string += "    category: " + json.dumps(cat) + "\n"
    string += "  },\n"
    
"""{
    id: "pm_motion.movebacksteps",
    spec: "move back %1 steps",
    inputs: ["%n"],
    shape: "stack",
    category: "pm_motion",
  }"""
print(string)
