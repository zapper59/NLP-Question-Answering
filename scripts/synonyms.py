import thesaurus as th
#from thesaurus import Word

def get_synonyms(word):
    print("syn", word)
    print(th.Word(word).synonyms(relevance=3, allowEmpty=False))

def get_antonyms(word):
    print("ant", word)
    print(th.Word(word).antonyms(relevance=3, allowEmpty=False))


if __name__ == '__main__':
    get_synonyms("sibling")
    get_synonyms("brother")
    get_antonyms("alive")
