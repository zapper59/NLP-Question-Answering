# NLP-Question-Answering

## Extracting Data Manually (files in qa_data)

This directory contains question and answer pairs for our testing and training
data sets. Each file follows the following standard:

- The name of the file is <name>.txt where <name> appears in name_indexer.json
  (e.g. jon_snow.txt)
- the first line is a question
- The second line is an answer
- The third line is the nth occurence of the answer in the context paragraph given by
  characters.json (e.g. characters[65][paragraphs][0] is the first context
  paragraph for Jon Snow).
- All nonempty lines up until the first empty line reference the first context
  paragraph. After a new line, all nonempty lines up until the second empty line reference
  the second context, and so on.
- Last line must be an empty line
- **Every context must have a question, answer and position triplet**

For example, if you are looking at Sansa in characters.json, it looks like this:

```
{'metadata': {},
 'name': 'Sansa Stark',
 'paragraphs': [{'context': 'Lady Sansa Stark is the eldest daughter of Lord '
                            'Eddard Stark of Winterfell and his wife Lady '
                            'Catelyn, sister of Robb, Arya, Bran, and Rickon '
                            'Stark, and "half-sister" of Jon Snow. Sansa '
                            'becomes well versed in politics and court '
                            'intrigue under the tutelage of Cersei Lannister '
                            'and Petyr Baelish, suffering but learning from '
                            'her traumatic experiences as a hostage of House '
                            "Lannister in King's Landing and House Bolton at "
                            'Winterfell. Alongside Jon Snow, Sansa takes back '
                            'Winterfell from House Bolton at the Battle of the '
                            'Bastards, becoming the new Lady of Winterfell. '},
                {'context': 'Sansa Stark is the eldest daughter and second '
                            'child of Lady Catelyn and Lord Eddard Stark, the '
                            'Warden of the North.\n'
                            'Sansa was born and raised at Winterfell. She has '
                            'an older brother, Robb, two younger brothers, '
                            'Bran and Rickon, a younger sister, Arya,and a " '
                            'bastard half-brother" Jon Snow, with whom she had '
                            "a distant relationship due to her mother's "
                            'influence(which, like her mother, Sansa later '
                            'regretted). Sansa enjoys proper "lady-like" '
                            'pursuits and is good at sewing, embroidering, '
                            'poetry, singing, dancing, literature, etiquette, '
                            'history, and music. When she was young she '
                            'dreamed of being a queen like Cersei Lannister, '
                            'and that just like in the epic songs she would '
                            'meet her knight in shining armor. She has '
                            "inherited her mother's Tully coloring, unlike all "
                            'of her siblings, and Lady Catelyn thinks Sansa '
                            'will be even more beautiful than she was when she '
                            'was younger. She is often seen in contrast with '
                            'her sister Arya, who has neither her looks nor '
                            'her accomplishments in feminine activities and '
                            'comportment.  '},
                {'context': 'Sansa is given praise by Septa Mordane after '
                            'exceeding in her sewing abilities, in contrast to '
                            'her sister Arya, who finds this tedious and '
                            'difficult. '}, ...
```

An example of a valid QA data file is:

```
Where does Sansa take back Winterfell from, alongside Jon Snow?
House Bolton
1
At which Battle does Sansa take back Winterfell?
Battle of the Bastards
1

Where was Sansa born and raised?
Winterfell
1
What did Sansa dream of being when she was young?
Queen
1

Who is Sansa given praise by, after exceeding in her sewing abilities?
Septa Mordane
1

```

The format_data.py script will take the data in qa_data and format the data so
that the BERT script from huggingface will accept it. This format is how SQuAD
formats its data.

