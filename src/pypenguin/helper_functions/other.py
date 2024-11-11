from pprint import pprint
import re

def escape_chars(input_string: str, chars_to_escape: list) -> str:
    # Escape backslashes first by doubling them up
    escaped_string = re.sub(r'\\', r'\\\\', input_string)
    
    # Escape each character in chars_to_escape by adding a backslash before it
    for char in chars_to_escape:
        escaped_string = re.sub(re.escape(char), r'\\' + char, escaped_string)
    
    return escaped_string

def ikv(data:dict): # Iterate through a dict with i(ndex of the pair), k(ey) and v(alue)
    return zip(
        range(len(data)),
        data.keys(),
        data.values(),
    )

def pp(obj): # pretty print with settings i like
    pprint(obj, sort_dicts=False)

def flipKeysAndValues(obj: dict): # self explanatory
    return {v:k for i,k,v in ikv(obj)}

def removeStringDuplicates(array):
    return dict.fromkeys(array).keys()

def customHash(obj):
    return hash(obj) % 1000

class WhatIsGoingOnError(Exception): # Just means its likely the dev's fault 
    pass
