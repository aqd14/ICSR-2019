"""
Visualization for the paper
"""

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from utils import tokenize, make_requirements
from cluster import cluster_requirements
from gensim.models import Doc2Vec
from sklearn.cluster import Birch
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

print(__doc__)

# Generating the sample data from make_blobs
# This particular setting has one distinct cluster and 3 clusters placed close
# together.
X, y = make_blobs(n_samples=500,
                  n_features=2,
                  centers=4,
                  cluster_std=1,
                  center_box=(-10.0, 10.0),
                  shuffle=True,
                  random_state=1)  # For reproducibility


# feature_paths = [os.path.join(os.getcwd(), 'clean', p) for p in ['clean-file-sharing-features.txt', 'clean-antivirus-features.txt', 'clean-browser-features.txt']]
# model_file_paths = [os.path.join(os.getcwd(), 'model', m) for m in ['model_file_sharing', 'model_antivirus', 'model_browser']]
# requirement_paths = [os.path.join(os.getcwd(), 'requirement', r) for r in ['file-sharing-requirements.txt', 'antivirus-requirements.txt', 'browser-requirements.txt']]
#
# boilerplates = [os.path.join(os.getcwd(), 'boilerplate', b) for b in ['boilerplate-file-sharing.csv', 'boilerplate-antivirus.csv', 'boilerplate-browser.csv']]

NUM_CLUSTERS = 5

feature_path = os.path.join(os.getcwd(), 'clean', 'clean-antivirus-features.txt')
model_path = os.path.join(os.getcwd(), 'model', 'model_antivirus')
# cluster_arr, score = cluster_requirements(model_path, feature_path, NUM_CLUSTERS)


features = tokenize(feature_path)

# load model
model = Doc2Vec.load(model_path)
# test_docs = [x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines()]

X = []
for d in features:
    X.append(model.infer_vector(d))
    # X.append(m.infer_vector(d, alpha=start_alpha, steps=infer_epoch))


range_n_clusters = [5]

for n_clusters in range_n_clusters:
    # Create a subplot with 1 row and 2 columns
    fig, ax2 = plt.subplots(1, 1)
    fig.set_size_inches(8, 5)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    # ax1.set_xlim([-0.1, 1])
    # # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # # plots of individual clusters, to demarcate them clearly.
    # ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = Birch(branching_factor=50, n_clusters=n_clusters, threshold=0.05, compute_labels=True)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)

    X = TSNE(n_components=2).fit_transform(X)
    # y_lower = 10
    # for i in range(n_clusters):
    #     # Aggregate the silhouette scores for samples belonging to
    #     # cluster i, and sort them
    #     ith_cluster_silhouette_values = \
    #         sample_silhouette_values[cluster_labels == i]
    #
    #     ith_cluster_silhouette_values.sort()
    #
    #     size_cluster_i = ith_cluster_silhouette_values.shape[0]
    #     y_upper = y_lower + size_cluster_i
    #
    #     color = cm.nipy_spectral(float(i) / n_clusters)
    #     ax1.fill_betweenx(np.arange(y_lower, y_upper),
    #                       0, ith_cluster_silhouette_values,
    #                       facecolor=color, edgecolor=color, alpha=0.7)
    #
    #     # Label the silhouette plots with their cluster numbers at the middle
    #     ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    #
    #     # Compute the new y_lower for next plot
    #     y_lower = y_upper + 10  # 10 for the 0 samples
    #
    # ax1.set_title("The silhouette plot for the various clusters.")
    # ax1.set_xlabel("The silhouette coefficient values")
    # ax1.set_ylabel("Cluster label")
    #
    # # The vertical line for average silhouette score of all the values
    # ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    #
    # ax1.set_yticks([])  # Clear the yaxis labels / ticks
    # ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')

    # Labeling the clusters
    # centers = clusterer.subcluster_centers_
    # # Draw white circles at cluster centers
    # ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
    #             c="white", alpha=1, s=200, edgecolor='k')
    #
    # for i, c in enumerate(centers):
    #     ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
    #                 s=50, edgecolor='k')

    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")

    # plt.suptitle(("Silhouette analysis for Birch clustering algorithm, "
    #               "n_clusters = %d" % n_clusters),
    #              fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()