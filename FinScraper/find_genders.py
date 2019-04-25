import json

male_pns=["he","him","his","himself"]
fem_pns=["she","her","hers","herself"]

with open('characters.json','r') as f:
    wiki = json.load(f)
    genders=[]

    for person in wiki:
        name = person['name']
        male_count = 0
        fem_count = 0
        for p in person['paragraphs']:
            for word in p['context'].lower().split():
                for pn in male_pns:
                    if word==pn:
                        male_count+=1
                for pn in fem_pns:
                    if word==pn:
                        fem_count+=1
        female=fem_count>male_count
        print(name, female, male_count, fem_count)
        genders.append({
            'name': name,
            'female': female
        })

    with open('genders.json','w') as of:
        json.dump(genders, of)

