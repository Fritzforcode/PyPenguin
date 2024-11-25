from pypenguin.database import opcodeDatabase
from pypenguin.helper_functions import ikv, pp

ity = []
ina = []
oty = []
ona = []
for i,k,v in ikv(opcodeDatabase):
    for j,l,w in ikv(v["inputTypes"]):
        if l not in ina: ina.append(l)
        if w not in ity: ity.append(w)
    for j,l,w in ikv(v["optionTypes"]):
        if l not in ona: ona.append(l)
        if w not in oty: oty.append(w)
    
pp(([ina, ity], [ona, oty]))
