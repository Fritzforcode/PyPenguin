from pypenguin.helper_functions import readJSONFile, ikv, pp

data = readJSONFile("temp.json")

s = []
for i, blockKey, block in ikv(data["targets"][1]["blocks"]):
    if block["opcode"] == "procedures_prototype":#"procedures_definition" or block["opcode"] == "procedures_definition_return":
        mut = block["mutation"]
        print(mut["proccode"])
        print("- warp", repr(mut["warp"]))
        print("- returns", repr(mut["returns"]))
        print("- edited", repr(mut["edited"]))
        print("- optype", repr(mut["optype"]))
        
