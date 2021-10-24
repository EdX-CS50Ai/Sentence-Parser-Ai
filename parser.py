import nltk
# nltk.download('punkt')
from nltk.tree import Tree
from nltk.tokenize import word_tokenize
import sys
import re

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
S -> NP VP | NP VP NP | NP VP NP NP | NP Conj NP VP | NP Conj VP NP | NP VP Conj NP VP | NP VP Conj VP NP | NP VP NP Conj NP VP | NP VP NP Conj VP NP
NP ->  Det Adj V | P N | P Det N | P Det Adj N | Det Adj Adj Adj N | Det Adj N | Adj N | Adv N | Det N | N 
VP -> V | V NP | | V NP | Adv V | V Adv | Adv V NP  | V NP Adv
PP -> P NP
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
    tokens = word_tokenize(sentence)
    # print(tokens)
    processed = []
    for word in tokens:
        # print(word.lower())
        has_alpha_numeric = False
        for ch in word:
            if ch.isalnum():
                has_alpha_numeric = True
        if has_alpha_numeric:
            processed.append(word.lower())

    # print(processed)
    return processed


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # tree.pretty_print()
    np = Tree('NP', tree)
    # print(np)
    return np


if __name__ == "__main__":
    main()
