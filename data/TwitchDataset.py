## ------ Influence Maximization over Twitch Dataset ------ ##
# We test ResQue Greedy over Twitch Dataset for influence maximization over a social network.
import os
import urllib.request
import gzip
import time
import random
import networkx as nx
import pickle
import numpy as np
import pandas as pd

# Step 1: Download and extract the dataset
def download_dataset(path='data/soc-twitch.txt.gz'):
    url = 'https://snap.stanford.edu/data/twitch.zip'
    if not os.path.exists(path):
        print("Downloading twitch dataset...")
        urllib.request.urlretrieve(url, path)
    else:
        print("twitch dataset already downloaded.")
    return path

# Step 2: Parse into a NetworkX graph
def load_graph_from_edges(folder_path, lang_code):
    """
    Loads a graph from twitch/<lang_code>/<lang_code>_edges.csv
    """
    edge_file = os.path.join(folder_path, lang_code, f"musae_{lang_code}_edges.csv")
    print(f"Loading edges from: {edge_file}")
    
    edges_df = pd.read_csv(edge_file)
    G = nx.from_pandas_edgelist(edges_df, source='from', target='to', create_using=nx.DiGraph())
    
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

# === Main pipeline ===
if __name__ == '__main__':
    data_path = download_dataset()
    lang_list = ["DE","ENGB","ES","FR","PTBR","RU"]
    for lang in lang_list:
        G = load_graph_from_edges("data/twitch/", lang)
        print(f"Saving graph {lang}...")
        with open(f"data/twitch_graph_{lang}.pkl", "wb") as f:
            pickle.dump(G, f)
        print(f"{lang} dataset saved!")