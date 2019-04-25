import argparse
import format_data
import json

parser = argparse.ArgumentParser()
parser.add_argument("query", help="query to use")
args = parser.parse_args()

def extract_cap_words(s):
    s = s[:-1]
    ss = s.split()
    ignore = ['Who', 'What', 'When', 'Where']
    ans = [w for w in ss if w[0].isupper() and w not in ignore]
    return ans

if __name__ == '__main__':
    # open characters.json
    with open(format_data.format_path('../FinScraper/characters.json'), 'r') as f:
        wiki = json.load(f)

    lw = extract_cap_words(args.query)

    # append query to every context of every character
    out = {'data': []}
    qc = 1
    for character in wiki:
        paras = []
        for c in character['paragraphs']:
            if all(cw in c['context'] for cw in lw):
                # create query with a real question, but fake others
                query = format_data.QA(qc, args.query, '', 0)
                paras.append({'context': c['context'], 'qas': [query.to_dict()]})
                qc += 1
        if paras:
            out['data'].append({'title': character['name'], 'paragraphs': paras})

    # write resulting json to file "query.json"
    with open(format_data.format_path('query.json'), 'w') as f:
        json.dump(out, f)
