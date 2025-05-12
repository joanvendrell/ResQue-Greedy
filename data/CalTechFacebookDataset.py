## ------ Influence Maximization over CalTechFacebbok Dataset ------ ##
# We test ResQue Greedy over CalTechFacebbok Dataset for influence maximization over a social network.
import networkx as nx
import pickle
import scipy.io

def mtx_to_pkl(input_file, output_file):
    # Load the .mtx file using scipy
    matrix = scipy.io.mmread(input_file)
    
    # Convert the matrix to a NetworkX graph (corrected method)
    G = nx.from_scipy_sparse_array(matrix)
    
    # Save the graph as a .pkl file
    with open(output_file, 'wb') as f:
        pickle.dump(G, f)
    
    print(f"Graph saved as {output_file}")

# Example Usage
input_file = "data/socfb-Caltech36.mtx"    # Replace with your .mtx file path
output_file = "data/cal_tech_facebook_graph.pkl"   # The .pkl output file
mtx_to_pkl(input_file, output_file)
