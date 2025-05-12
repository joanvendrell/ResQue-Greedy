## ------ Influence Maximization over Youtube Dataset ------ ##
# We test ResQue Greedy over Youtube Dataset for influence maximization over a social network.
import networkx as nx
import pickle
import argparse

def text_to_pkl(input_file, output_file):
    # Initialize an empty graph (undirected)
    G = nx.Graph()
    with open(input_file, "r") as file:
        for line in file:
            # Skip header lines starting with #
            if line.startswith("#"):
                continue
            # Split the line into two nodes
            node1, node2 = map(int, line.strip().split())
            G.add_edge(node1, node2)
    
    # Save the graph as a standard pickle file (.pkl)
    with open(output_file, 'wb') as f:
        pickle.dump(G, f)
    
    print(f"Graph saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample subgraphs and compute reachability.")
    parser.add_argument("--input_file", type=str,  default="data/youtube_ungraph.txt", help="Input txt file")
    parser.add_argument("--output_file", type=str, default="data/youtube_graph.pkl", help="Output pkl file")

    args = parser.parse_args()
    text_to_pkl(args.input_file, args.output_file)

