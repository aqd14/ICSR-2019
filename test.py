import os

cluster_paths = [os.path.join(os.getcwd(), 'cluster', m) for m in ['cluster_file_sharing.txt', 'cluster_antivirus.txt', 'cluters_browser.txt']]

clusters = []

with open(cluster_paths[0]) as f:
    content = f.read().replace('[', '').replace(']', re)