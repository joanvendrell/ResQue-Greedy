## ------- Fault-Detection Mechanism ----- ##
import numpy as np
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from auxiliary.Auxiliary import get_combinations, compute_coverage

# Fault-detection mechanism
def fault_detection_coverage(input_data,S,e,path_curvature,set_curvature,tau,strategy):
    if strategy == "ResQue":
        curvature = path_curvature[-1] if path_curvature else 0
        if curvature < max(set_curvature,default=0):
            return True
    elif strategy == "Modularity":
        f_S = len(compute_coverage(input_data,S)); f_e = len(compute_coverage(input_data,[e]))
        f_S_e = len(compute_coverage(input_data,S+[e]))
        if f_S_e <= (f_e + f_S)*tau:
            return True
    elif strategy == "Probabilistic":
        gamma = max(max(path_curvature,default=0),max(set_curvature,default=0))
        if np.random.rand(1) <= gamma/(1+gamma):
            return True
    elif strategy == "Random":
        if np.random.rand(1) >= 0.5:
            return True
    return False

def fault_detection_reachability(G,reachability_dict,S,e,path_curvature,set_curvature,tau,strategy):
    if strategy == "ResQue":
        curvature = path_curvature[-1] if path_curvature else 0
        if curvature <= max(set_curvature,default=0):
            return True
    elif strategy == "Modularity":
        f_S = prepare_probabilistic_reachability_sets(G, reachability_dict, S, seed)
        f_e = prepare_probabilistic_reachability_sets(G, reachability_dict, [e], seed)
        f_S_e = prepare_probabilistic_reachability_sets(G, reachability_dict, S+[e], seed)
        if f_S_e <= (f_e + f_S)*tau:
            return True
    elif strategy == "Probabilistic":
        gamma = max(max(path_curvature,default=0),max(set_curvature,default=0))
        if np.random.rand(1) <= gamma/(1+gamma):
            return True
    elif strategy == "Random":
        if np.random.rand(1) >= 0.5:
            return True
    return False

# Re-wiring strategy
def rewiring(groundset,selected,trace_curvature,strategy):
    if strategy == "Random":
        options = get_combinations(groundset, len(selected))
        return list(random.choice(options)), trace_curvature
    else:
        differences = [abs(trace_curvature[i] - trace_curvature[i-1]) for i in range(1, len(trace_curvature))]
        if not differences:
            return selected, trace_curvature
        element = selected[differences.index(max(differences))]
        selected.remove(element)
        trace_curvature.remove(trace_curvature[differences.index(max(differences))])
        return selected, trace_curvature