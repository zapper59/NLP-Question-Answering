import re
from relations import relation_regex
from metadata import find_best_name_match
from relations import resolve_relation

def process_question(q):
    print('>>>Answering question:', f'"{q}"')
    q=q.lower()
    form=r'(who )?(is )?(?P<character>.*)(oldest|youngest)?(living|dead|alive)? +(?P<relation>'+relation_regex+r') *\??$'
    match=re.match(form, q)
    if not match:
        form=r'(who )?(is )?(?P<character>.*)(?P<relation>)?\??$'
        match=re.match(form, q)
    if match:
        #print(match)
        char=match.group('character')
        relation=match.group('relation')
        names=find_best_name_match(char)['matches']
        print(char, "||", relation, "||", names)
        if len(names)>0:
            if relation and len(relation)>0:
                names = resolve_relation(names, relation)
            print('### Answer:', names)
        else:
            print('### Answer was not found')
    else:
        print('### Format not recognized')
    print()


if __name__ == '__main__':
    print(relation_regex)
    process_question("Who is arya's father?")
    process_question("Who is the three eyed raven?")
    process_question("Who is the Mother of dragons?")
    process_question("Who is Peter Dinklage?")
    process_question("Who is Peter Dinklage's grandfather?")
