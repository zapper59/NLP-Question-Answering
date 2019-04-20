import json
from pprint import pprint

with open('names.txt', 'r') as f:
    d = {}
    count = 0
    for rl in f.readlines():
        l = rl.strip()
        d[l.lower().replace(' ', '_')] = count
        count += 1

with open('name_indexer.json', 'w') as g:
    json.dump(d, g)
