import argparse
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

class QAv2(QA):
    def __init__(self, i, q, a, p, is_impos):
        QA.__init__(self, i, q, a, p)
        self.is_impos = is_impos

    def to_dict(self):
        d = {'id': self.id,
             'question': self.question,
             'answers': [{'answer_start': self.char_idx, 'text': self.answer}],
             'is_impossible': self.is_impos}
        return d


# Return a dictionary {character_name: {context_idx: QA(v2)s that are all answerable}}}
def parse_data(manual_data_files, name_idxr, characters, path, is_v2):
    all_char_qas = {}
    for rawtf in manual_data_files:
        name = os.path.splitext(rawtf)[0]
        character_id = name_idxr[name]
        data = characters[character_id]

        with open(path + name + '.txt', 'r') as h:
            # qas := [{id, question, answers}]
            # answers := [{answer_start, text}]

            char_qas = {}
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
                    mask = 'Q' * len(a)
                    char_idx = curr_context.replace(a, mask, int(p)-1).find(a)
                    qa = QAv2(qid, q, a, char_idx, False) if is_v2 else QA(qid, q, a, char_idx)
                    qas.append(qa.to_dict())
                    q_counter += 1
                else:
                    print('Error: state not 0, 1 or 2')
                    exit(0)

                if not line:
                    char_qas[context_idx] = qas
                    qas = []
                    q_counter = 0
                    context_idx += 1
                else:
                    state = (state + 1)%3
        all_char_qas[name] = char_qas
    return all_char_qas

def format_data(files, name_idxr, characters, path, is_v2):
    out = {'data': []}
    qadict = parse_data(files, name_idxr, characters, path, is_v2)

    for name in qadict:
        csqas = []
        char_paras = characters[name_idxr[name]]['paragraphs']
        for cont_idx in qadict[name]:
            cont = char_paras[cont_idx]['context']
            csqas.append({'context': cont, 'qas': qadict[name][cont_idx]})
        outele = {'title': name, 'paragraphs': csqas}
        out['data'].append(outele)
    return out


def format_path(p):
    basepath = os.path.dirname(__file__)
    return os.path.join(basepath, p)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--v2", action='store_true', help="Format as SQuAD v2.0 data")
    args = parser.parse_args()

    # get data for all characters here
    with open(format_path('../FinScraper/characters.json'), 'r') as f:
        wiki = json.load(f)

    # get mappings from character name to index into JSON list
    with open(format_path('../FinScraper/name_indexer.json'), 'r') as g:
        name_indexer = json.load(g)

    train_path = format_path('../qa_data/training/')
    train_files = os.listdir(train_path)
    # print(train_files)
    train_out = format_data(train_files, name_indexer, wiki, train_path, args.v2)
    pprint(train_out)

    with open(format_path('training.json'), 'w') as f:
        json.dump(train_out, f)

    test_path = format_path('../qa_data/testing/')
    test_files = os.listdir(test_path)
    # print(test_files)
    test_out = format_data(test_files, name_indexer, wiki, test_path, args.v2)

    with open(format_path('testing.json'), 'w') as f:
        json.dump(test_out, f)
