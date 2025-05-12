## Implementation of Submodular Local Search
import itertools
import numpy as np
import random
import networkx as nx
from tqdm import tqdm
from .Auxiliary import *

import random

def local_search_submodular_maximization_reachability(G, reachability_dict, k, seed, initial_value=None, epsilon=1e-5, max_iters=100):
    E = set(G.nodes)
    # Initial random subset of size k
    if initial_value:
        T = set(initial_value)
        current_value = prepare_probabilistic_reachability_sets(G, reachability_dict, initial_value, seed)
    else:
        T = set(random.sample(list(E), k))
        current_value = prepare_probabilistic_reachability_sets(G, reachability_dict, list(T), seed)

    improved = True; num_iters = 0; query_time = 1; results = [T]
    progress_bar = tqdm(total=max_iters, desc="Processing", ncols=100)
    while improved or num_iters <= max_iters:
        progress_bar.update(1)
        improved = False
        for e_out in T:
            for e_in in E - T:
                candidate = (T - {e_out}) | {e_in}
                candidate_value = prepare_probabilistic_reachability_sets(G, reachability_dict, list(candidate), seed)
                query_time += 1
                num_iters += 1
                results.append(candidate_value)
                if candidate_value > current_value * (1 + epsilon):
                    T = candidate
                    current_value = candidate_value
                    improved = True
                    break
            if improved:
                break
    progress_bar.close()
    return T, current_value, query_time, results


def local_search_submodular_maximization_coverage(input_data, k, initial_value=None, epsilon=1e-5, max_iters=100):
    E = set(input_data.keys())
    # Initial random subset of size k
    if initial_value:
        T = set(initial_value)
        current_value = len(compute_coverage(input_data, initial_value))
    else:
        T = set(random.sample(list(E), k))
        current_value = len(compute_coverage(input_data, list(T)))
    
    improved = True; num_iters=0; query_time = 1; results = [T]
    while improved or num_iters<=max_iters:
        improved = False
        for e_out in T:
            for e_in in E - T:
                candidate = (T - {e_out}) | {e_in}
                candidate_value = len(compute_coverage(input_data, list(candidate)))
                query_time += 1
                num_iters += 1
                results.append(candidate_value)
                if candidate_value > current_value * (1 + epsilon):
                    T = candidate
                    current_value = candidate_value
                    improved = True
                    break
            if improved:
                break

    return T, current_value, query_time, results
