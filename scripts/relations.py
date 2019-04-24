#TODO gender/ synonym matching/

import re
import json 
import sys
import spacy
from spacy import displacy

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://the-professor.cs.utexas.edu:7687", auth=("neo4j", "password"))

relations=["sibling", "child", "parent", "spouse", "uncle", "cousin", "in-law", "nephew", "parent-in-law", "child-in-law", "grandparent", "grandchild", "great-grandparent", "great-grandchild"]
def get_relatives(names, relation):
    print("Finding", relation, "of", names)
    with driver.session() as tx:
        ans=[]
        if relation == "sibling":
            rel_type="-[:IS_SIBLING_OF]-"
        elif relation == "child":
            names=get_relatives(names,"spouse").union(names) #ex: robin arryn
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
