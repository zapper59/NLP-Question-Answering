import json
import os
from pprint import pprint

class QA(object):
    def __init__(self, i, q, a, p):
        self.id = i
        self.question = q
        self.answer = a
        self.char_idx = p

    def to_dict(self):
        d = {'id': self.id,
             'question': self.question,
             'answers': [{'answer_start': self.char_idx, 'text': self.answer}]}
        return d

def format_data(files, name_idxr, characters, path):
    out = {'data': []}
    for rawtf in files:
        name = os.path.splitext(rawtf)[0]
        character_id = name_idxr[name]
        data = characters[character_id]
        out['data'].append({'title': data['name']})

        with open(path + name + '.txt', 'r') as h:
            # create lqas structure
            # lqas := [{context, qas}]
            # qas := [{id, question, answers}]
            # answers := [{answer_start, text}]

            context_idx = 0
            lqas = []
            qas = []
            q = ''
            a = ''
            p = 0
            state = 0
            q_counter = 0
            for rawline in h.readlines():
                line = rawline.strip()
                curr_context = data['paragraphs'][context_idx]['context']
                if state == 0:
                    q = line
                elif state == 1:
                    a = line
                elif state == 2:
                    p = line
                    qid = str(character_id) + 'a' + str(context_idx) + 'a' + str(q_counter)
                    xmask = 'X' * len(a)
                    char_idx = curr_context.replace(a, xmask, int(p)-1).find(a)
                    qas.append(QA(qid, q, a, char_idx).to_dict())
                    q_counter += 1
                else:
                    print('Error: state not 0, 1 or 2')
                    exit(0)

                if not line:
                    context_idx += 1
                    lqas.append({'context': curr_context, 'qas': qas})
                    qas = []
                    q_counter = 0
                else:
                    state = (state + 1)%3
        out['data'][-1]['paragraphs'] = lqas
    return out

# get data for all characters here
with open('FinScraper/characters.json', 'r') as f:
    wiki = json.load(f)

# get mappings from character name to index into JSON list
with open('FinScraper/name_indexer.json', 'r') as g:
    name_indexer = json.load(g)

train_path = 'qa_data/training/'
train_files = os.listdir(train_path)
# print(train_files)
train_out = format_data(train_files, name_indexer, wiki, train_path)

with open('training.json', 'w') as f:
    json.dump(train_out, f)

test_path = 'qa_data/testing/'
test_files = os.listdir(test_path)
# print(test_files)
test_out = format_data(test_files, name_indexer, wiki, test_path)

with open('testing.json', 'w') as f:
    json.dump(test_out, f)
