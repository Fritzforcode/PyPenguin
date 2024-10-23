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

class WhatIsGoingOnError(Exception): # Just means its likely the dev's fault 
    pass

