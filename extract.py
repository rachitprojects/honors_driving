
import json
from ast import literal_eval

with open("emo.txt") as test:
    x = test.read()
    p = (x.split('         "'))
    for l in range(len(p)):
        # print(l)
        if p[l]:
            print(literal_eval(p[l][1:]))
            print("\n")
