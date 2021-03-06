import argparse
import collections
import json
import operator

parser = argparse.ArgumentParser()
parser.add_argument("preds", help="path to predictions json file")
args = parser.parse_args()

### Get answer
with open(args.preds, 'r') as f:
    preds = json.load(f)

freq = collections.Counter()
m = {}

for i in preds:
    ans = preds[i][0]['text']
    score = preds[i][0]['probability']
    if ans:
        freq[ans] += 1
        if ans in m:
            m[ans] = max(m[ans], score)
        else:
            m[ans] = score

topm = sorted(m.items(), key=operator.itemgetter(1), reverse=True)

with open('predictions.txt', 'a') as f:
    if topm:
        candidate = topm[0]
        f.write(candidate[0] + '\n')
    else:
        # no answer
        f.write('\n')
