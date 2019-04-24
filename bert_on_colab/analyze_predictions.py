import argparse
import collections
import json
import operator

parser = argparse.ArgumentParser()
parser.add_argument("preds", help="path to predictions json file")
args = parser.parse_args()

with open(args.preds) as f:
    preds = json.load(f)

freq = collections.Counter()
sumscores = {}
for i in preds:
    ans = preds[i]['text']
    score = preds[i]['probability']
    freq[ans] += 1
    if ans in sumscores:
        sumscores[ans] += score
    else:
        sumscores[ans] = score

avgscores = {}
for text, c in freq.most_common(3):
    avgscores[text] = sumscores[text]/c

top_avgscores = sorted(avgscores.items(), key=operator.itemgetter(1), reverse=True)
print(top_avgscores)
