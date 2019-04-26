'''
utility functions
'''

import spacy
from collections import Counter

from spacy.tokenizer import Tokenizer

BOILERPLATE = 'System shall provide the user with the ability to {} {} {}'


def tokenize(path):
    """
    Tokenize every line in a file
    :param path: path to file
    :return: an array of tokens
    """
    nlp = spacy.load('en_core_web_sm')
    tokenizes = []
    with open(path) as f:
        for line in f.readlines():
            tokenizer = Tokenizer(nlp.vocab)
            tokens = [token.text for token in tokenizer(line.replace('system should ', '').replace('\n', ''))]
            tokenizes.append(tokens)

    return tokenizes


def make_requirements(elements):
    """
    make a requirement from boilerplate elements
    :param elements: DataFrame containing verb, object, and additional information of a requirement
    :return: a list of requirements created by combining elements value
    """

    verbs = []
    objs = []
    details = []

    for df in elements:
        for _, row in df.iterrows():
            verbs.append(row['verb'])
            objs.append(row['object'])
            details.append(row['detail'])

    requirements = []
    for i in range(len(verbs)):
        for j in range(len(objs)):
            for k in range(len(details)):
                if i != j and j != k:
                    requirements.append(make_requirement(verbs[i], objs[j], details[k]))

    return requirements


def make_requirement(verb, obj, detail):
    return BOILERPLATE.format(verb, obj, detail)

# c = Counter()
# for line in open('f').splitlines():
#     c.update(line.split())
# print(c)