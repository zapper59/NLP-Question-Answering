"""Jorge Hernandez wrote this for the second NLP project involving creating a database of triples.
I am using and modifying the code he wrote to create dependency parse triples of questions"""

#%%
import spacy
import os
import json
# import textacy
from spacy.symbols import root

#%%
# dir_name = './Questions/'
# directory = os.fsencode(dir_name)

# nlp = spacy.load('en_core_web_lg')
nlp = spacy.load("en")
# coref = spacy.load('en_coref_md')

#%%
def valid_triple(left, right):
    invalid_pos = set(['VERB', 'PUNCT', 'ADV', 'PART'])
    invalid_tags = set(['IN', 'CC', 'DT', 'WDT'])

    # this is meant to be a workaround for some noun tokens
    # some of the noun chunks that were merged are labeled
    # as determiners if the first word is a determiner.
    l_dt = (left.tag_ == 'DT' or left.tag_ == 'WDT') and len(left.text.strip().split()) > 1 
    r_dt = (right.tag_ == 'DT' or right.tag_ == 'WDT') and len(right.text.strip().split()) > 1

    inv_tags = left.tag_  not in invalid_tags and right.tag_ not in invalid_tags
    inv_pos = left.pos_ not in invalid_pos and right.pos_ not in invalid_pos
    not_eq = left.text != right.text
    return inv_pos and (inv_tags or (l_dt or r_dt)) and not_eq

def gather_triples(docs):
    triples = []

    for chunk in docs.noun_chunks:
        chunk.merge()
    
    for ent in docs.ents:
        ent.merge()

    incomplete_tags = set(['IN', 'DET'])

    for sent in docs.sents:
        vrbs = [w for w in sent if w.pos_ == 'VERB']

        for verb in vrbs:
            for l in verb.lefts:
                # so prepositions aren't good in triples
                # look at the prepositions children
                left = list(l.children)
                left = left[0] if left and l.tag_ in incomplete_tags else l

                for r in verb.rights:
                    right = list(r.children)
                    right = right[0] if right and r.tag_ in incomplete_tags else r

                    if valid_triple(left, right):
                        triples.append((left.text, verb.text, right.text))
    return triples

    def gather_triples(docs):
        triples = []

        for chunk in docs.noun_chunks:
            chunk.merge()
        
        for ent in docs.ents:
            ent.merge()

        incomplete_tags = set(['IN', 'DET'])

        for sent in docs.sents:
            vrbs = [w for w in sent if w.pos_ == 'VERB']

            for verb in vrbs:
                for l in verb.lefts:
                    # so prepositions aren't good in triples
                    # look at the prepositions children
                    left = list(l.children)
                    left = left[0] if left and l.tag_ in incomplete_tags else l

                    for r in verb.rights:
                        right = list(r.children)
                        right = right[0] if right and r.tag_ in incomplete_tags else r

                        if valid_triple(left, right):
                            triples.append((left.text, verb.text, right.text))
        return triples

def resolve_prnn(json):
    for subsection, subsection_txt in json.items():
        coref_txt = coref(subsection_txt)
        if coref_txt._.has_coref:
            json[subsection] = coref_txt._.coref_resolved

def print_triples(triples):
    for trip in triples:
        print('{} | {} | {}'.format(*trip))

def write_triples(triples, file_name):
    with open(file_name, 'w') as fi:
        json.dump(triples, fi)
#%%
# for file in os.listdir(directory):
#     file_name = os.fsdecode(file)
#     with open(dir_name + file_name, 'r') as fi:
#         json_fi = json.load(fi)
#         resolve_prnn(json_fi)
#         animal_name = ' '.join(map(lambda s: s.capitalize(), file_name.split('.')[0].split('-')))
#         output_fi_name = './spacy_animal_triples/' + file_name
#         json_output = {}
#         for subsection, subsection_txt in json_fi.items(): 
#             docs = nlp(subsection_txt)
#             # triples = list(map(lambda t: (t[0].text, t[1].text, t[2].text) , gather_triples(docs)))
#             triples = gather_triples(docs)
#             # print('[{}]\n'.format(subsection))
#             # print_triples(triples)
#             # print()
#             json_output[subsection] = triples
#         write_triples(json_output, output_fi_name)

text_file = "Questions.txt"
output_file = "Triples.txt"

with open(text_file, 'r') as fi_r:
    with open(output_file, 'w') as fi_w:
        for line in fi_r:
            doc = nlp(line)
            triples = []
            for token in doc:
                cur_word = (token.text, token.tag_, token.dep_)
                triples.append(cur_word)
            fi_w.write(str(triples) + "\n")
