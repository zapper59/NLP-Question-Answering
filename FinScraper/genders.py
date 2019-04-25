import json

people={}
with open("genders.json",'r') as f:
    gender_json=json.load(f)
    for p in gender_json:
        people[p['name']] = p['female']

def is_person_female(person):
    print(person)
    return people[person]


if __name__ == '__main__':
    print(is_person_female("Jon Snow"))
    print(is_person_female("Arya Stark"))
