## Implementation of http://proceedings.mlr.press/v139/balkanski21a/balkanski21a.pdf
import itertools
import numpy as np
import random
import networkx as nx
from tqdm import tqdm
from .Auxiliary import *
from multiprocessing import Pool


##################### REACHABILITY PROBLEM ########################

def process_element(subset_elements, G, reachability_dict, seed):
    return prepare_probabilistic_reachability_sets(G, reachability_dict, subset_elements, seed)

def compute_singleton(a, G, reachability_dict, seed):
    return (a, prepare_probabilistic_reachability_sets(G, reachability_dict, [a], seed))

def OPT_submodular_upper_bound_reachability(G, reachability_dict, seed, num_workers, k):
    """
    Method 3 for submodular maximization upper bound.
    
    Returns:
        float: upper bound on the optimal value
    """
    print("Computing the instance approximation...")
    # 1st - Create the ground_set and sort the singletons values
    ground_set = list(G.nodes()); n = len(ground_set)
    #singleton_values = [(a, prepare_probabilistic_reachability_sets(G, [a], p, num_samples, seed, num_workers)) for a in  tqdm(ground_set, desc="Computing singletons")]
    with Pool(processes=num_workers) as pool:
        singleton_values = list(tqdm(pool.starmap(compute_singleton, 
                                                 [(a, G, reachability_dict, seed) for a in ground_set]), 
                                    total=len(ground_set), 
                                    desc="Computing singletons"))
    sorted_elements = [a for a, _ in sorted(singleton_values, key=lambda x: -x[1])]
    print("Singletons computed!")
    # Precompute prefixes A_i = {a1, ..., ai}
    f_a_i = [a for _,a in sorted(singleton_values, key=lambda x: -x[1])]
    #f_A_i = [prepare_probabilistic_reachability_sets(G, sorted_elements[:i+1], p, num_samples, seed, num_workers) for i in tqdm(range(len(sorted_elements)), desc="Computing extended sets")]
    subset_elements_list = [sorted_elements[:i+1] for i in range(len(sorted_elements))]
    with Pool(processes=num_workers) as pool:
        f_A_i = list(tqdm(pool.starmap(process_element, 
                                       [(subset, G, reachability_dict, seed) for subset in subset_elements_list]), 
                          total=len(sorted_elements), 
                          desc="Processing reachability sets"))
    print("Joints computed!")
    # Start the iteration
    v_list = []; i_j_prev = -1
    for j in range(k):
        # i' = min f(A_i) - sum v_l > v, so i' \in {i+1,i+2,...}
        max_vj = 0
        for i in range(i_j_prev+1, n):
            f_a_i_j = f_a_i[i]
            rhs = f_A_i[i] - sum(v_list)
            if rhs >= f_a_i_j:
                i_j_prev = i
                v_list.append(f_a_i_j)
    return sum(v_list)


##################### COVERAGE PROBLEM ########################

def process_element_coverage(input_data, subset_elements):
    return len(compute_coverage(input_data, subset_elements))

def compute_singleton_coverage(input_data, a):
    return (a, len(compute_coverage(input_data, [a])))

def OPT_submodular_upper_bound_coverage(input_data, k, num_workers=5):
    """
    Method 3 for submodular maximization upper bound.

    Returns:
        float: upper bound on the optimal value
    """
    #print("Computing the instance approximation...")
    # 1st - Create the ground_set and sort the singletons values
    ground_set = list(input_data.keys()); n = len(ground_set)
    singleton_values = [(a, len(compute_coverage(input_data, [a]))) for a in ground_set]
    #with Pool(processes=num_workers) as pool:
    #    singleton_values = list(tqdm(pool.starmap(compute_singleton_coverage, 
    #                                             [(input_data,a) for a in ground_set]), 
    #                                total=len(ground_set), 
    #                                desc="Computing singletons"))
    sorted_elements = [a for a, _ in sorted(singleton_values, key=lambda x: -x[1])]
    #print("Singletons computed!")
    # Precompute prefixes A_i = {a1, ..., ai}
    f_a_i = [a for _,a in sorted(singleton_values, key=lambda x: -x[1])]
    f_A_i = [len(compute_coverage(input_data, sorted_elements[:i+1])) for i in range(len(sorted_elements))]
    #subset_elements_list = [sorted_elements[:i+1] for i in range(len(sorted_elements))]
    #with Pool(processes=num_workers) as pool:
    #    f_A_i = list(tqdm(pool.starmap(process_element_coverage, 
    #                                   [(input_data, subset) for subset in subset_elements_list]), 
    #                      total=len(sorted_elements), 
    #                      desc="Processing reachability sets"))
    #print("Joints computed!")
    # Start the iteration
    v_list = []; i_j_prev = -1
    for j in range(k):
        # i' = min f(A_i) - sum v_l > v, so i' \in {i+1,i+2,...}
        max_vj = 0
        for i in range(i_j_prev+1, n):
            f_a_i_j = f_a_i[i]
            rhs = f_A_i[i] - sum(v_list)
            if rhs >= f_a_i_j:
                i_j_prev = i
                v_list.append(f_a_i_j)
    return max(sum(v_list),max(f_A_i))