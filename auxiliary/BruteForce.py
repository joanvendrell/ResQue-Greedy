## ----- Brute Force Algorithm ----- ##
from .Auxiliary import compute_coverage
from itertools import chain, combinations

def brute_force_optimal_coverage(input_data, k):
    best_selection = None
    best_coverage = 0
    query_time = 0
    for subset in combinations(list(input_data.keys()), k):
        current_coverage = len(compute_coverage(input_data,subset))
        if current_coverage > best_coverage:
            best_coverage = current_coverage
            best_selection = subset
        query_time += 1
    
    return list(best_selection),query_time
