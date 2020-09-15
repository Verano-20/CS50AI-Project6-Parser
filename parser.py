import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | Det N | Det Adj N | Adj NP | NP P NP | NP Adv
VP -> V | VP NP | NP VP | VP P | VP P NP | VP Det NP | VP Conj VP | Adv VP | VP Adv
Adj -> Adj Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    word_tok = nltk.word_tokenize(sentence)
    words = [word.lower() for word in word_tok if word.isalpha()]
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NPChunks = []
    for leaf in tree.treepositions('leaves'):
        node = leaf[:-1] # Leaf's parent
        # Find next NP up
        while tree[node].label() != 'NP':
            if tree[node].label() == 'S':
                break
            node = node[:-1]
        # Check if NP contains another NP
        if tree[node].label() == 'NP':
            NPC = True
            for subtree in tree[node].subtrees():
                if subtree == tree[node]:
                    continue
                if subtree.label() == 'NP':
                    NPC = False
                    break
            # Add NPC to list
            if NPC:
                if tree[node] not in NPChunks:
                    NPChunks.append(tree[node])
    return NPChunks


if __name__ == "__main__":
    main()
