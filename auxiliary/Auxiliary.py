## -------- Auxiliary algorithms --------- ##
import itertools
import numpy as np
import random
import networkx as nx
from concurrent.futures import ThreadPoolExecutor

# Function to get all combinations of size k
def get_combinations(values, k):
    return list(itertools.combinations(values, k))
    
# Function to get all permutations
def get_permutations(values):
    return list(itertools.permutations(values))

## ---- Reachability tools ---- ##
def prepare_probabilistic_reachability_sets(G, reachability_dict, nodes=None, seed=None):
    if seed is not None:
        random.seed(seed)
    if nodes is None:
        nodes = list(G.nodes())
    f_sum = 0
    for sub_graph in reachability_dict.keys():
        reached_points = set()
        for node in nodes:
            reached_points.update(reachability_dict[sub_graph][str(node)])
        f_sum += len(reached_points)/len(reachability_dict.keys())
    return f_sum 

def compute_marginals_reachability(G, reachability_dict, selected, seed=None):
    marginals = np.zeros(len(G.nodes())); expansion_curvature = np.zeros(len(G.nodes()))
    queries = 0
    reachability_sets = prepare_probabilistic_reachability_sets(G, reachability_dict, selected, seed)
    for i in range(len(G.nodes())):
        if i not in selected:
            independent_reachability_i = prepare_probabilistic_reachability_sets(G, reachability_dict, [i], seed)
            reachability_sets_i = prepare_probabilistic_reachability_sets(G, reachability_dict, selected+[i], seed)
            # Add the gain
            marginals[i] = reachability_sets_i - reachability_sets
            # Compute trace curvature
            expansion_curvature[i] = 1-(reachability_sets_i-reachability_sets)/max(independent_reachability_i,0.0001)
            # Gather computational information
            queries += 1
    return marginals, expansion_curvature, queries

## ---- Greedy tools ---- ##
# Function to compute the coverage given a selected amount of points
# input_data = dict{allocation_points: target_points}, selected = [allocation_points_idx,...]
def compute_coverage(input_data, selected):
    coverage = set()
    if not selected:
        return coverage
    for point in selected:
        coverage.update(set(input_data[point]))
    return coverage

# Function to compute the marginals
def compute_marginals(input_data, selected):
    keys =  list(input_data.keys())
    marginals = np.zeros(len(keys)); expansion_curvature = np.zeros(len(keys))
    queries = 0
    for i in range(len(keys)):
        if i not in selected:
            # Exclude already covered targets
            covered_targets = compute_coverage(input_data, selected)
            independent_coverage_i = compute_coverage(input_data, [keys[i]])
            # Add the gain
            marginals[i] = len(independent_coverage_i - covered_targets)
            # Compute trace curvature
            expansion_curvature[i] = 1-len(independent_coverage_i-covered_targets)/max(len(independent_coverage_i),0.0001)
            # Gather computational information
            queries += 1
    return marginals, expansion_curvature, queries


    
