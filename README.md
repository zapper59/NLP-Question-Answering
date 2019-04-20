# NLP-Question-Answering

## Extracting Data Manually (files in qa_data)

This directory contains question and answer pairs for our testing and training
data sets. Each file follows the following standard:

- The name of the file is <name>.txt where <name> appears in name_indexer.json
  (e.g. jon_snow.txt)
- the first line is a question
- The second line is an answer
- The third line is the position of the answer in the context paragraph given by
  characters.json (e.g. characters[65][paragraphs][0] is the first context
  paragraph for Jon Snow)
- All nonempty lines up until the first empty line reference the first context
  paragraph. After a new line, all nonempty lines up until the second empty line reference
  the second context, and so on.

The format_data.py script will take the data in qa_data and format the data so
that the BERT script from huggingface will accept it. This format is how SQuAD
formats its data.
