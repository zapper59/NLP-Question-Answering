import json
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from relations import is_relation_supported

#TODO Add family names as aliases for their members
# answers "Who is the youngest Stark son?"
#TODO Get age or birthday
#TODO get death status

metadata={}
alias_map={}
alias_list=set()
a_padding=""#"*****************************************************************"

with open('../FinScraper/characters_meta.json', 'r') as f:
    alias_fields=["Titles", "Also known as", "Portrayed by"]
    wiki = json.load(f)
    for p in wiki:
        name = p['name']
        metadata[name]=p
        meta = p["metadata"]
        name_a = name.lower().strip()
        alias_map[name_a]=set([name])
        alias_list.add(name_a+a_padding)
        for alias in alias_fields:
            if alias in meta:
                for a in meta[alias].split("\n"):
                    a = a.lower().strip()
                    if not a in alias_map:
                        alias_map[a]=set()
                    alias_map[a].add(name)
                    alias_list.add(a+a_padding)

def find_best_name_match(phrase):
    p=phrase
    phrase=phrase.lower()
    phrase+="*****************************************************************"
                          #"david bradley (disguised as walder frey"
                          #"princess of dragonstone (formerly; throne userped by aegon ii)"
    #matches=process.extract(phrase, alias_list, scorer=fuzz.partial_token_set_ratio, limit=100)
    matches=process.extract(phrase, alias_list, scorer=fuzz.partial_ratio, limit=100)
    #matches = [(m[0].strip(a_padding[0]), m[1]) for m in matches]
    print()
    print(matches[:20])
    ans=set()
    ans_a=set()
    ans_a_len=-1
    for m in matches:
        if m[1] == matches[0][1] and len(m[0])>=ans_a_len:
            #print(m[0])
            #print(alias_map[m[0]])
            if len(m[0])>ans_a_len:
                ans_a_len = len(m[0])
                ans=set()
                ans_a=set()
            ans.update(alias_map[m[0]])
            ans_a.add(m[0])

    return {
            "phrase": p,
            "alias": ans_a,
            "matches": ans,
            "ratio": matches[0][1]
    }

def is_token_special(phrase):
    phrase=re.sub(r"[^a-z]", "", phrase.lower())
    return is_relation_supported(phrase) or phrase in ["living","dead","alive","oldest","youngest"]

def remove_relations(phrase):
    arr=phrase.split()
    end=len(arr)-1
    while(is_token_special(arr[end])):
        end-=1
    return ' '.join(arr[:end+1])

if __name__ == '__main__':
    #print(alias_map)
    print(find_best_name_match("Who is the three eyed raven?"))
    print(find_best_name_match("ned's wife?"))
    print(find_best_name_match("ned's "))
    print(find_best_name_match("ned's ******"))
    print(find_best_name_match("Sansa's oldest brother"))
    print(find_best_name_match("Sansa's oldest *****"))
    print(find_best_name_match("Who is Peter Dinklage?"))
    print(find_best_name_match("Who is The mother of dragons' mother?"))
    print(find_best_name_match("the oldest Lannister?"))
    print(find_best_name_match("the king in the north?"))
    print(find_best_name_match("the lord of casterly rock"))
    print(remove_relations("Who is The mother of dragons?"))
    print(remove_relations("Who is The mother of dragons' mother?"))
    print(find_best_name_match("Who is the daughter of Lady Catlyn and Lord Eddard?"))
