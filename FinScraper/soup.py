from bs4 import BeautifulSoup
import re
import sys
import json
import string
from requests import get

import codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)

print(sys.stdout.encoding)
data = []

def has_class_but_no_id(tag):
        return tag.has_attr('class') and not tag.has_attr('id')

with open("names.txt") as f:

    for name in f:
        print(name)
        url = "https://gameofthrones.fandom.com/wiki/" + name.strip().replace(" ", '_')
        html = get(url).text.encode('ascii', errors='ignore')
        #html = html.encode('')
        print(str(html).encode('utf-8'))
        #soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(html, 'html5lib')
        text = soup.find(id="mw-content-text")
        print(type(text))
        print("****************")
        print(text.encode('utf-8'))
        paras=[]
        for para in text('p', recursive=False):
            para_t=""
            print("*****")
            for string in para.stripped_strings:
                para_t+=string.encode('utf-8').decode()+" "
                #print((string).encode('utf-8'))
            para_t=re.sub(r"(\[\d*\])|( [,.])", "", para_t)
            print(para_t)
            if len(para_t) != 0:
                paras.append({
                    'context': para_t
                })
        data.append({
            'name': name.strip(),
            'url': url,
            'paragraphs': paras
        })

    with open('characters.json','w') as outfile:
        json.dump(data, outfile)

        #exit()
