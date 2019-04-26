import numpy as np
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

with open(os.path.join(os.getcwd(), 'clean', 'clean-antivirus-features.txt')) as f:
    all_features = f.readlines()


cosine_sim_scores = []

tfidf_vectorizer = TfidfVectorizer()
with open(os.path.join(os.getcwd(), 'requirement','antivirus-requirements.txt')) as f:
    for generated_feature in f.readlines()[:500]:
        appended_features = [generated_feature] + all_features
        tfidf_matrix = tfidf_vectorizer.fit_transform(appended_features)
        cosine_sim_scores.append(np.mean(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)))


X = np.arange(len(cosine_sim_scores))

# fig,ax = plt.subplots(1)

plt.figure(figsize=(8,4))
plt.bar(X, cosine_sim_scores, width=0.3, color='#4286f4')
plt.xlabel("generated requirement id")
plt.ylabel("cosine similarity td-idf score")
# plt.gca().axes.get_xaxis().set_visible(False)

cosine_sim_scores.sort()

plt.axhline(y=cosine_sim_scores[400], color='r', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.show()

print('Finished!')

