'''
Generate new requirements
'''

from utils import tokenize, make_requirements
from cluster import cluster_requirements

import spacy
import pandas as pd
import numpy as np
import os

nlp = spacy.load('en_core_web_sm')

# path
feature_paths = [os.path.join(os.getcwd(), 'clean', p) for p in ['clean-file-sharing-features.txt', 'clean-antivirus-features.txt', 'clean-browser-features.txt']]
model_file_paths = [os.path.join(os.getcwd(), 'model', m) for m in ['model_file_sharing', 'model_antivirus', 'model_browser']]
requirement_paths = [os.path.join(os.getcwd(), 'requirement', r) for r in ['file-sharing-requirements.txt', 'antivirus-requirements.txt', 'browser-requirements.txt']]

boilerplates = [os.path.join(os.getcwd(), 'boilerplate', b) for b in ['boilerplate-file-sharing.csv', 'boilerplate-antivirus.csv', 'boilerplate-browser.csv']]

NUM_CLUSTERS = 5

for model_path, feature_path, bl, requirement_path in zip(model_file_paths, feature_paths, boilerplates, requirement_paths):
    print('START GENERATING REQUIREMENTS FOR {}\n'.format(model_path))
    features = tokenize(feature_path)

    cluster_arr, score = cluster_requirements(model_path, feature_path, NUM_CLUSTERS)
    # print(cluster_arr)

    df = pd.read_csv(os.path.join(os.getcwd(), 'boilerplate', bl), sep=',')
    # indexes[i] contains indices of all requirements belong to cluster (i+1)
    indices = [np.where(cluster_arr == i) for i in range(NUM_CLUSTERS)]
    # print(cluster_1)

    with open(requirement_path, 'w') as writer:
        # randomly pick 3 requirements from each cluster for 10 times to make 100 x 6 = 60 requirements
        for i in range(100):
            for ind in indices:
                # print(ind)
                triple = np.random.choice(ind[0], 3)
                bl_1 = df[df.id == triple[0]].head(1)
                bl_2 = df[df.id == triple[1]].head(1)
                bl_3 = df[df.id == triple[2]].head(1)

                requirements = make_requirements([bl_1, bl_2, bl_3])
                writer.writelines('%s\n' % r for r in requirements)
    print('----------------END-----------------\n\n\n')






    # generate new requirements by swapping parts in pair files
    # generate 10 requirement x 10 times x total number of combination = 100 requirements
    # df = pd.read_csv(os.path.join(os.getcwd(), 'boilerplate', bl), sep=',')
    # print('START GENERATING REQUIREMENTS FOR {}\n'.format(model_path))
    # id = randint(0, len(features) - 1)
    # original = df[df.id == id]
    # vector = model.infer_vector(features[id])
    # print('selected feature = {}\n'.format(str(features[id])))
    # for (ix, matched_percentage) in model.docvecs.most_similar([vector]):
    #     similar = df[df.id == ix]
    #     # create two new requirements from combining each pair of similar requirements
    #     # print(original['verb'])
    #     # print(original['object'])
    #     # print(original['detail'])
    #     for _, row1 in original.iterrows():
    #         for _, row2 in similar.iterrows():
    #             print(BOILERPLATE.format(row1['verb'], row2['object'], row2['detail']))
    #             print(BOILERPLATE.format(row2['verb'], row1['object'], row1['detail']))
            # for v, s in zip(original[], similar):
            #     print(v, s)
            # print(ix, matched_percentage, features[ix])


# vector = model.infer_vector(features[0])
# for (ix, percentage) in model.docvecs.most_similar([vector]):
#     print(ix, features[ix])
#
#
# print('-------------------------')
#
# vector = model.infer_vector(features[1])
# for (ix, percentage) in model.docvecs.most_similar([vector]):
#     print(ix, features[ix])