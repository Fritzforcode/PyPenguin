from pypenguin.helper_functions import readJSONFile, ikv

data = readJSONFile("temp.json")

s = []
for i, blockKey, block in ikv(data["targets"][1]["blocks"]):
    if block["opcode"] not in s:
        print(block["opcode"])
        s.append(block["opcode"])
