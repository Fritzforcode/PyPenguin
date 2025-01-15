from pypenguin.utility.utility import BlockSelector

# -----------------------
# Utility Classes
# -----------------------
class BlockSelector:
    count = 0

    def __init__(self):
        self.id = BlockSelector.count
        BlockSelector.count += 1

    def __eq__(self, other):
        return isinstance(other, BlockSelector) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"BlockSelector::{self.id}"
    
    def copy(self):
        new = BlockSelector()
        new.id = self.id
        return new

# -----------------------
# Data Structure Manipulation Functions
# -----------------------
def getSelectors(obj):
    selectors = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, BlockSelector):
                selectors.append(k)
            if isinstance(v, BlockSelector):
                selectors.append(v)
            else:
                selectors += getSelectors(v)
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, BlockSelector):
                selectors.append(v)
            else:
                selectors += getSelectors(v)
    return selectors

def editDataStructure(obj, conditionFunc: callable, conversionFunc: callable):
    if isinstance(obj, dict):
        newObj = {}
        for key, value in obj.items():
            newKey = conversionFunc(key) if conditionFunc(key) else editDataStructure(key, conditionFunc, conversionFunc)
            newValue = conversionFunc(value) if conditionFunc(value) else editDataStructure(value, conditionFunc, conversionFunc)
            newObj[newKey] = newValue
        return newObj

    if isinstance(obj, (list, tuple, set)):
        newObj = type(obj)()
        for item in obj:
            newItem = conversionFunc(item) if conditionFunc(item) else editDataStructure(item, conditionFunc, conversionFunc)
            newObj.append(newItem)
        return newObj
    return obj

def getDataAtPath(data, path:list[str|int]):
    """
    Retrieve data from a nested structure (dictionaries/lists) using a path.
    """
    current = data
    for key in path:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return None
    return current
