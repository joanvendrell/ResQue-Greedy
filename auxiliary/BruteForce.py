## ----- Brute Force Algorithm ----- ##
from Auxiliary import compute_coverage

def brute_force_optimal_coverage(allocation_points, target_points, radius, k):
    best_selection = None
    best_coverage = 0
    query_time = 0
    for subset in combinations(range(len(allocation_points)), k):
        current_coverage = len(compute_coverage(allocation_points[list(subset)], target_points, radius))
        if current_coverage > best_coverage:
            best_coverage = current_coverage
            best_selection = subset
        query_time += 1
    
    return list(best_selection),query_time