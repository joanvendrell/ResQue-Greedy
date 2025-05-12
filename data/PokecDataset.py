## ------ Influence Maximization over Pokec Dataset ------ ##
# We test ResQue Greedy over Pokec Dataset for influence maximization over a social network.
import os
import urllib.request
import gzip
import time
import random
import networkx as nx
import pickle
import numpy as np

# Step 1: Download and extract the dataset
def download_pokec(path='soc-pokec.txt.gz'):
    url = 'https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz'
    if not os.path.exists(path):
        print("Downloading Pokec dataset...")
        urllib.request.urlretrieve(url, path)
    else:
        print("Pokec dataset already downloaded.")
    return path

# Step 2: Parse into a NetworkX graph
def load_pokec_graph(path):
    print("Loading graph...")
    G = nx.DiGraph()
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            u, v = map(int, line.strip().split())
            G.add_edge(u, v)
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

# Step 3: Prepare coverage sets
def prepare_coverage_sets(G, k_hop=1):
    print(f"Preparing coverage sets with k={k_hop}...")
    coverage_sets = {}
    for node in G.nodes():
        # 1-hop or k-hop neighborhood using BFS
        neighbors = set(nx.single_source_shortest_path_length(G, node, cutoff=k_hop).keys())
        neighbors.discard(node)  # remove self
        if neighbors:
            coverage_sets[node] = neighbors
    print(f"Prepared coverage sets for {len(coverage_sets)} nodes.")
    return coverage_sets

# === Main pipeline ===
if __name__ == '__main__':
    pokec_path = download_pokec()
    G_pokec = load_pokec_graph(pokec_path)
    coverage_dict = prepare_coverage_sets(G_pokec, k_hop=1)

    # Optional: Save for later use
    with open('data/pokec_coverage.pkl', 'wb') as f:
        pickle.dump(coverage_dict, f)

    print("Saved coverage sets to 'pokec_coverage.pkl'")