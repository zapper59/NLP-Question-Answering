import argparse
import collections
import json
import operator

parser = argparse.ArgumentParser()
parser.add_argument("preds", help="path to predictions json file")
args = parser.parse_args()

:
### Get answer
with open(args.preds, 'r') as f:
    preds = json.load(f)

freq = collections.Counter()

for i in preds:
    ans = preds[i][0]['text']
    if ans:
        freq[ans] += 1

with open('predictions.txt', 'a') as f:
    f.write(freq.most_common(1)[0][0])
