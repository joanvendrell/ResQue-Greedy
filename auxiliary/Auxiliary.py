## -------- Auxiliary algorithms --------- ##
import itertools
import numpy as np

# Function to get all combinations of size k
def get_combinations(values, k):
    return list(itertools.combinations(values, k))
    
# Function to get all permutations
def get_permutations(values):
    return list(itertools.permutations(values))

# Greedy tools:
# Function to compute the coverage given a selected amount of points
def compute_coverage(allocation_points, target_points, radius):
    coverage = set()
    if allocation_points.ndim == 1:
        allocation_points = [allocation_points]
    for point in allocation_points:
        distances = np.linalg.norm(target_points - point, axis=1)
        covered_targets = set(np.where(distances <= radius)[0])
        coverage.update(covered_targets)
    return coverage

# Function to compute classical curvature definition
def curvature(allocation_points, P, radius, k):
    I = all_combinations(P) #independent_sets
    minimum = 10000000
    for e in P:
        for S in I:
            num = len(compute_coverage(allocation_points[S.union(e)], P, radius)) - len(compute_coverage(allocation_points[S], P, radius))
            den = len(compute_coverage(allocation_points[e], P, radius)) - len(compute_coverage({}, P, radius))
            Delta = num/den
            if Delta<=minimum:
                minimum = Delta
    return 1-minimum

# Function to compute the marginals
def compute_marginals(allocation_points, target_points, radius, selected):
    marginals = np.zeros(len(allocation_points))
    curvatures = np.zeros(len(allocation_points))
    queries = 0
    for i in range(len(allocation_points)):
        if i not in selected:
            # Exclude already covered targets
            covered_targets = compute_coverage(allocation_points[selected], target_points, radius)
            new_coverage = compute_coverage(allocation_points[[i]], target_points, radius)
            # Add the gain
            marginals[i] = len(new_coverage - covered_targets)
            # Compute trace curvature
            curvatures[i] = 1-len(new_coverage- covered_targets)/max(len(compute_coverage(allocation_points[[i]], target_points, radius)),0.0001)
            # Gather computational information
            queries += 1
    return marginals, curvatures, queries
    
