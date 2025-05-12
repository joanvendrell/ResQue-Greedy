import os
import random
import pickle
import json
import argparse
import networkx as nx
from tqdm import tqdm

# --- Function to sample and save a graph
def _single_sample_reachability_and_save(G, p, folder_path, sample_id):
    sampled_edges = [e for e in G.edges() if random.random() < p]
    G_sample = nx.DiGraph() if G.is_directed() else nx.Graph()
    G_sample.add_nodes_from(G.nodes())
    G_sample.add_edges_from(sampled_edges)
    
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"graph_{sample_id}.gpickle")
    with open(file_path, "wb") as f:
        pickle.dump(G_sample, f)

# --- Function to compute reachability and save results
def compute_reachability_from_samples_and_save(folder_path, nodes, output_file):
    reachability_results = {}
    graph_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".gpickle")])
    for file_name in tqdm(graph_files):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path,"rb") as f:
            G_sample = pickle.load(f)
        sample_reachability = {}
        for node in nodes:
            if node in G_sample:
                if G_sample.is_directed():
                    reachable = nx.descendants(G_sample, node)
                else:
                    reachable = set(nx.node_connected_component(G_sample, node))
                reachable.discard(node)
                sample_reachability[node] = list(reachable)
            else:
                sample_reachability[node] = []
        reachability_results[file_name] = sample_reachability
    with open(output_file, "w") as f:
        json.dump(reachability_results, f, indent=2)

# --- Main execution script
def main(args):
    # Load the graph
    with open(args.graph_path, "rb") as f:
        G = pickle.load(f)
    nodes = list(G.nodes())
    # Sampling and saving graphs
    save_folder = args.save_folder
    random.seed(args.seed)
    for i in range(args.num_samples):
        _single_sample_reachability_and_save(G, args.p, save_folder, i)
    print(f"{args.num_samples} graphs Sampled!")
    # Compute reachability from saved samples
    output_file = args.output_file
    compute_reachability_from_samples_and_save(save_folder, nodes, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample subgraphs and compute reachability.")
    parser.add_argument("--graph_path", type=str, required=True, help="Path to the input graph .pkl file")
    parser.add_argument("--p", type=float, required=True, help="Edge sampling probability")
    parser.add_argument("--num_samples", type=int, required=True, help="Number of subgraphs to sample")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--save_folder", type=str, default="sampled_graphs", help="Folder to save sampled graphs")
    parser.add_argument("--output_file", type=str, default="reachability_results.json", help="Output JSON file")

    args = parser.parse_args()
    main(args)

## python3 GraphReachabilitySetting.py --graph_path data/twitch_graph_ES.pkl --p 0.1 --num_samples 1000 --seed 42 --save_folder data_processed/sampled_twitch_graphs --output_file data_processed/reachability_twitch.json 