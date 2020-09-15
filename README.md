# CS50AI-Project6-Parser

This is my solution to Parser.

parser.py will take one of the provided sentences (or user input) and parse the sentence to generate one or more syntax tree(s), while extracting noun phrase chunks.

Context-free grammer rules were added to parse all of the sentences provided while avoiding parsing grammatically incorrect sentences where possible.

The np_chunk algorithm works from the leaves of the syntax tree (the words) upwards until it encouters a noun-phrase branch, and then validates if it is a noun phrase chunk by checking all other of its subtrees. A noun phrase chunk is a noun phrase that does not contain another noun phrase.
