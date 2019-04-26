'''
Clustering software requirements (as a sentence) using doc2vec
'''

import spacy
from spacy.tokenizer import Tokenizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
import os

nlp = spacy.load('en_core_web_sm')

paths = ['clean-file-sharing-features.txt', 'clean-file-manager-features.txt', 'clean-antivirus-features.txt', 'clean-browser-features.txt']
model_file_paths = ['model_file_sharing', 'model_file_manager', 'model_antivirus', 'model_browser']

for model_path, path in zip(model_file_paths, paths):
    features = []
    with open(path) as f:
        for line in f.readlines():
            tokenizer = Tokenizer(nlp.vocab)
            tokens = [token.text for token in tokenizer(line.replace('\n', ''))]
            features.append(tokens)
            # print(tokens)

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(features)]
    model = Doc2Vec(documents, vector_size=20, window=2, min_count=1, workers=4)
    # remove temp variables to save memory
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    fname = get_tmpfile(os.path.join(os.getcwd(), 'model', model_path))
    model.save(fname)