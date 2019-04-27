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
             'answers': [],
             'is_impossible': self.is_impos}
        if not self.is_impos:
            d['answers'].append({'answer_start': self.char_idx, 'text': self.answer})
        return d
    
    def to_dict_is_impossible(self):
        d = {'id': self.id,
             'question': self.question,
             'answers': [],
             'is_impossible': True}
        return d


# Return a dictionary {character_name: {context_idx: List[QA]}}}
# Every QA(v2) is answerable
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
                    qas.append(qa)
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

'''
Definitions:
    A context "c" is _related_ to a question "q" if we think the context
    has a high chance of containing the answer to "q".
'''


# Takes "Jon Snow" to "jon_snow"
def format_name(name):
    return '_'.join(name.lower().split())

def related_heuristic(q, context):
    '''
    q: question string
    context: context string
    Returns: True if context is related, and False otherwise.
    '''
    q = q[:-1]
    q_words = q.split()
    ignore = ['Who', 'What', 'When', 'Where', 'At', 'In', 'Of']
    cap_words = [w for w in q_words if w[0].isupper() and w not in ignore]
    return all(w in context for w in cap_words)

def get_related_contexts(k, q, q_name, q_idx, characters):
    '''
    k: int
    q: question string
    q_name: name of who "q" came from
    q_idx: index of context which "q" came from in q_name
    characters: JSON object of characters
    Retuns: a list of AT MOST "k" tuples in the form (char_name, context_idx) related to "q"
    Note: takes the first "k" found
    '''
    related_conts = []
    for char in characters:
        name = format_name(char['name'])
        cont_idx = 0
        for cont in char['paragraphs']:
            # don't include the 
            if q_name == name and q_idx == cont_idx:
                continue
            context = cont['context']
            if related_heuristic(q, context):
                related_conts.append((name, cont_idx))
            cont_idx += 1
    if len(related_conts) < k:
        return related_conts
    else:
        return related_conts[0:k]

def format_data(files, name_idxr, characters, path, is_v2):
    out = {'data': []}
    qadict = parse_data(files, name_idxr, characters, path, is_v2)

    # add training data (of unanswerable questions) to dictionary
    if is_v2:
        qa_imposs = {}
        for name in qadict:
            for cont_idx in qadict[name]:
                qas = qadict[name][cont_idx]
                for qa in qas:
                    qad = qa.to_dict_is_impossible()
                    rel_conts = get_related_contexts(5,
                            qa.to_dict()['question'], name, cont_idx,
                            characters)
                    for rname, rcidx in rel_conts:
                        if rname in qa_imposs:
                            if rcidx in qa_imposs[rname]:
                                if qa not in qa_imposs[rname][rcidx]:
                                    qa_imposs[rname][rcidx].add(qa)
                            else:
                                qa_imposs[rname][rcidx] = {qa}
                        else:
                            qa_imposs[rname] = {rcidx: {qa}}

    # add all training QAs
    for name in name_idxr:
        contexts = characters[name_idxr[name]]['paragraphs']
        char_qas = []
        if name in qadict:
            for cont_idx in qadict[name]:
                qas = [qa.to_dict() for qa in qadict[name][cont_idx]]
                if is_v2:
                    # if character's context has question from both dicts
                    try:
                        more_qas = list(qa_imposs[name][cont_idx])
                        qas += [q.to_dict_is_impossible() for q in more_qas]
                    # elif character's context only has questions from qadict
                    except Exception:
                        pass
                char_qas.append({'context': contexts[cont_idx]['context'],
                    'qas': qas})
            outele = {'title': name, 'paragraphs': char_qas}
            out['data'].append(outele)
        # if character's context only has questions from qa_imposs
        elif is_v2 and name in qa_imposs:
            for cont_idx in qa_imposs[name]:
                qas = [qa.to_dict_is_impossible() for qa in qa_imposs[name][cont_idx]]
                char_qas.append({'context': contexts[cont_idx]['context'],
                    'qas': qas})
            outele = {'title': name, 'paragraphs': char_qas}
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
    train_out = format_data(train_files, name_indexer, wiki, train_path, args.v2)

    with open(format_path('training.json'), 'w') as f:
        json.dump(train_out, f)

    test_path = format_path('../qa_data/testing/')
    test_files = os.listdir(test_path)
    test_out = format_data(test_files, name_indexer, wiki, test_path, args.v2)

    with open(format_path('testing.json'), 'w') as f:
        json.dump(test_out, f)
