#TODO gender/ synonym matching/

import re
import json 
import sys
import spacy
from spacy import displacy
from neo4j import GraphDatabase

from genders import is_person_female

driver = GraphDatabase.driver("bolt://the-professor.cs.utexas.edu:7687", auth=("neo4j", "password"))


#basic relations
relations=["sibling", "child", "parent", "spouse", "uncle", "cousin", "in-law", "nephew", "parent-in-law", "child-in-law", "grandparent", "grandchild", "great-grandparent", "great-grandchild"]

#maps from relation to basic relation.  If val[1] is defined it represents is_female on filtering returned values
#there are some repeats here, so search on more_relations before basic relations
more_relations={
        "brother":     ["sibling", False],
        "sister":      ["sibling", True],
        "son":         ["child", False],
        "daughter":    ["child", True],
        "father":      ["parent", False],
        "mother":      ["parent", True],
        "husband":     ["spouse", False],
        "wife":        ["spouse", True],
        "uncle":       ["uncle", False],
        "aunt":        ["uncle", True],
        "nephew":      ["nephew", False],
        "niece":       ["nephew", True],
        "grandfather": ["grandparent", False],
        "grandmother": ["grandparent", True]
}

relation_regex='|'.join(relations)+'|'+'|'.join(more_relations)

def is_relation_supported(relation):
    return relation in relations or relation in more_relations

#USE THIS ONE
# Supports gendered relations
def resolve_relation(names, relation):
    fem=None
    if relation in more_relations:
        fem=more_relations[relation][1]
        relation=more_relations[relation][0]
    found=get_relatives(names, relation)

    if found is None:
        return found
    return set(filter(lambda x: is_person_female(x)==fem, found))

#given names and a basic relation find matching characters
def get_relatives(names, relation):
    print("Finding", relation, "of", names)

    if relation == "sibling":
        rel_type="-[:IS_SIBLING_OF]-"
    elif relation == "child":
        names=get_relatives(names,"spouse").union(names) #ex: robin arryn
        print("Finding child of both:", names)
        rel_type="<-[:IS_CHILD_OF]-"
    elif relation == "parent":
        rel_type="-[:IS_CHILD_OF]->"
    elif relation == "spouse":
        rel_type="-[:IS_MARRIED_TO]-"
    elif relation == "uncle":
        return get_relatives(get_relatives(names, "parent"), "sibling")
    elif relation == "cousin":
        return get_relatives(get_relatives(names, "uncle"), "child")
    elif relation == "nephew":
        return get_relatives(get_relatives(names, "sibling"), "child")
    elif relation == "in-law":
        in_law=get_relatives(get_relatives(names,"spouse"), "sibling")
        in_law=in_law.union(get_relatives(get_relatives(names,"sibling"), "spouse"))
        return in_law.union(get_relatives(in_law,"spouse"))
    elif relation == "parent-in-law":
        return get_relatives(get_relatives(names,"spouse"), "parent")
    elif relation == "child-in-law":
        return get_relatives(get_relatives(names,"spouse"), "nephew")
    elif relation == "grandparent":
        return get_relatives(get_relatives(names,"parent"), "parent")
    elif relation == "grandchild":
        return get_relatives(get_relatives(names,"child"), "child")
    elif relation == "great-grandparent":
        return get_relatives(get_relatives(names,"grandparent"), "parent")
    elif relation == "great-grandchild":
        return get_relatives(get_relatives(names,"grandchild"), "child")
    else:
        print("NOT FOUND", names, relation) #TODO
        return names

    with driver.session() as tx:
        ans=[]
        for name in names:
            query = f"match (n:Person){rel_type}(s:Person) where n.name =~ '(?i).*{name}.*' return s"
            q_ret = tx.run(query)
            #print(type(q_ret))
            #print(q_ret)
            for match in q_ret.data():
                #print(type(match))
                #print(match)
                ans.append(dict(match['s'])['name'])
        return set(ans)




if __name__ == '__main__':
    print(is_relation_supported("sibling"))
    print(is_relation_supported("aunt"))
    print(is_relation_supported("x"))

    print("**** ", get_relatives(["Lothar Frey"], "sibling"))
    print("**** ", get_relatives(["Lothar Frey"], "parent"))
    print("**** ", get_relatives(["Walder Frey"], "spouse"))
    print("**** ", get_relatives(["Walder Frey"], "child"))
    print("**** ", get_relatives(["Sansa Stark"], "parent"))
    print("**** ", get_relatives(["Catelyn Stark"], "uncle"))
    print("**** ", get_relatives(["Sansa Stark"], "cousin"))
    print("**** ", get_relatives(["Catelyn Stark"], "nephew"))
    print("**** ", get_relatives(["Lysa Arryn"], "nephew"))
    print("**** ", get_relatives(["Jon Arryn"], "child-in-law"))
    print("**** ", get_relatives(["Jon Arryn"], "in-law"))
    print("**** ", get_relatives(["Eddard Stark"], "parent-in-law"))
    print("**** ", get_relatives(["Hoster Tully"], "grandchild"))
    print("**** ", get_relatives(["Arya Stark"], "grandparent"))
    # TODO I can't find any great-grandparent relations in the database
    print("**** ", get_relatives(["Jon Snow"], "great-grandparent"))
    print("**** ", get_relatives(["Aegon V Targaryen"], "great-grandchild"))

    print("**** ", resolve_relation(["Arya Stark"], "brother"))
    print("**** ", resolve_relation(["Arya Stark"], "sister"))
    print("**** ", resolve_relation(["Eddard Stark"], "daughter"))
