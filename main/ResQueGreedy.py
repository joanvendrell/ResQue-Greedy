## ----- ResQue Greedy Algorithm ----- ###
import numpy as np
from FaultDetection import fault_detection, rewiring
from Auxiliary import compute_marginals

# Auxiliary
def greedy_step(marginals):
    return np.argmax(marginals)


# Main Algorithm
def greedy_coverage(allocation_points, target_points, radius, k, strategy = "Classical"):
    selected = []
    trace_curvature = []; curvatures = []  
    query_time = 0; rewires = 0
    while len(selected)<k:
        # Re-wired
        if strategy != "Classical" and rewires<2:
            if fault_detection(selected,trace_curvature,curvatures,strategy):
                selected,trace_curvature = rewiring(list(range(len(allocation_points))),selected,trace_curvature,strategy)
                rewires += 1
        # Apply Greedy Algorithm
        marginals,curvatures,queries = compute_marginals(allocation_points, target_points, radius, selected)
        e = greedy_step(marginals)
        selected.append(e)
        trace_curvature.append(curvatures[e])
        query_time += queries
    return selected,query_time,rewires,trace_curvature