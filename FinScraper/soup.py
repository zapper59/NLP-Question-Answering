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
        #print(str(html).encode('utf-8'))
        #soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(html, 'html5lib')
        text = soup.find(id="mw-content-text")
        #print(type(text))
        print("****************")
        #print(text.encode('utf-8'))
        paras=[]
        
        if True: #TODO
            for para in text('p', recursive=False):
                para_t=""
                print("*****")
                for string in para.stripped_strings:
                    para_t+=string.encode('utf-8').decode()+" "
                    #print((string).encode('utf-8'))
                para_t=re.sub(r"\[\d*\]", "", para_t)
                para_t=re.sub(r" ,", ",", para_t)
                para_t=re.sub(r" \.", ".", para_t)
                print(para_t)
                if len(para_t) != 0:
                    paras.append({
                        'context': para_t
                    })

        metadata={}
        person={
            'name': name.strip(),
            'url': url,
            'paragraphs': paras,
            'metadata': metadata
        }
        
        print("$$$$$")
        if False: #TODO
            for key in text.find('aside', class_='portable-infobox').find_all('h3'):
                key_text = ' '.join([s for s in key.stripped_strings])
                print(key_text)
                value_div = key.parent.find('div', class_='pi-data-value', recursive=False)
                #for s in value_div.strings:
                    #print("###", s)
                val_text = ' '.join([s for s in value_div.stripped_strings])
                val_text = re.sub(r" ,", ",", val_text)
                val_text = re.sub(r" \.", ".", val_text)
                print(val_text)
                metadata[key_text] = val_text

        data.append(person)
        #exit()

    #with open('characters_meta.json','w') as outfile:
    with open('characters.json','w') as outfile:
        json.dump(data, outfile)

        #exit()
