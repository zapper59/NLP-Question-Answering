import argparse
from pprint import pprint
import json

parser = argparse.ArgumentParser()
parser.add_argument("name", help="name of character (lowercase and underscores only")
args = parser.parse_args()

with open('name_indexer.json', 'r') as f:
    idxr = json.load(f)

idx = idxr[args.name]

with open('characters.json', 'r') as f:
# with open('characters_meta.json', 'r') as f:
    wiki = json.load(f)

pprint(wiki[idx])
