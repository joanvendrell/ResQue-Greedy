## ----- ResQue Greedy Algorithm ----- ###
import numpy as np
import sys
import os
from tqdm import tqdm
from .FaultDetection import fault_detection_coverage,fault_detection_reachability,rewiring
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from auxiliary.Auxiliary import *

# Auxiliary
def greedy_step(marginals, input_data):
    idx = np.argmax(marginals)
    return list(input_data.keys())[idx]


# Main Algorithm
# input_data = dict{allocation_points: target_points}
def greedy_coverage(ground_set, input_data, k, strategy = "Classical", rewiring_limit = 100000, tau = 0.8, monitor=True):
    selected = []
    path_curvature = []; set_curvature = []  
    query_time = 0; rewires = 0; iters = 0
    r_iter=0; controlled_iters=0; last_seq_greedy_curvatures=None; accumulated_cond=0
    last_greedy_S = None
    while len(selected)<k:
        iters += 1
        # Apply Greedy Algorithm
        S_i_minus_1 = selected
        marginals, curvature_expansion, queries = compute_marginals(input_data, selected)
        e = greedy_step(marginals, input_data)
        selected.append(e)
        path_curvature.append(curvature_expansion[e])
        set_curvature.append(max(curvature_expansion))
        query_time += queries
        # Monitoring sufficient conditions
        if monitor and r_iter == 1:
            delta_rsg = len(compute_coverage(input_data,S_i_minus_1+[e])) - len(compute_coverage(input_data,S_i_minus_1))
            delta_sg = len(compute_coverage(input_data,last_greedy_S)) - len(compute_coverage(input_data,S_i_minus_1))
            accumulated_cond += delta_rsg - delta_sg
        # Re-wired        
        if strategy == "Classical":
            pass
        elif strategy != "Classical" and rewires<rewiring_limit:
            if fault_detection_coverage(input_data,S_i_minus_1,e,path_curvature,set_curvature,tau,strategy):
                # Re-wiring procedure
                selected,path_curvature = rewiring(list(input_data.keys()),selected,path_curvature,strategy)
                rewires += 1
            # Monitoring sufficient conditions
            if monitor:
                if rewires == 1 and r_iter == 0:
                    last_seq_greedy_curvatures = curvature_expansion; r_iter += 1
                    last_greedy_S = S_i_minus_1
                elif rewires >= 1 and r_iter > 0:
                    r_iter += 1; lhs = (curvature_expansion[e] - last_seq_greedy_curvatures[e])*len(compute_coverage(input_data,[e]))
                    if accumulated_cond >= lhs:
                        controlled_iters += 1
                        accumulated_cond += lhs
    if monitor:
        uncertainty = 1-controlled_iters/max(1,r_iter-1)
    else:
        uncertainty = 1
    return selected,query_time,rewires,max(set_curvature),uncertainty

def greedy_reachability(G,reachability_dict,k,strategy="Classical",rewiring_limit=100000,seed=None,num_workers=3,tau=0.5,monitor=True):
    selected = []
    path_curvature = []; set_curvature = []  
    query_time = 0; rewires = 0; iters = 0
    r_iter=0; controlled_iters=0; last_seq_greedy_curvatures=None; accumulated_cond=0
    last_greedy_S = None
    while len(selected)<k:
        iters += 1
        # Apply Greedy Algorithm
        S_i_minus_1 = selected
        marginals, curvature_expansion, queries = compute_marginals_reachability(G,reachability_dict,selected,seed)
        e = np.argmax(marginals) #greedy_step(marginals, input_data)
        selected.append(e)
        path_curvature.append(curvature_expansion[e])
        set_curvature.append(max(curvature_expansion))
        query_time += queries
        # Monitoring sufficient conditions
        if monitor and r_iter == 1:
            delta_rsg = prepare_probabilistic_reachability_sets(G, reachability_dict, S_i_minus_1+[e], seed) - prepare_probabilistic_reachability_sets(G, reachability_dict, S_i_minus_1, seed)
            delta_sg = prepare_probabilistic_reachability_sets(G, reachability_dict, last_greedy_S, seed) - prepare_probabilistic_reachability_sets(G, reachability_dict, S_i_minus_1, seed)
            accumulated_cond += delta_rsg - delta_sg
        # Re-wired        
        if strategy == "Classical":
            pass
        elif strategy != "Classical" and rewires<rewiring_limit:
            if fault_detection_reachability(G,reachability_dict,S_i_minus_1,e,path_curvature,set_curvature,tau,strategy):
                # Re-wiring procedure
                selected,path_curvature = rewiring(list(G.nodes()),selected,path_curvature,strategy)
                rewires += 1
            # Monitoring sufficient conditions
            if monitor:
                if rewires == 1 and r_iter == 0:
                    last_seq_greedy_curvatures = curvature_expansion; r_iter += 1
                    last_greedy_S = S_i_minus_1
                elif rewires >= 1 and r_iter > 0:
                    r_iter += 1; lhs = (curvature_expansion[e] - last_seq_greedy_curvatures[e])*prepare_probabilistic_reachability_sets(G, reachability_dict, [e], seed)
                    if accumulated_cond >= lhs:
                        controlled_iters += 1
                        accumulated_cond += lhs
    if monitor:
        uncertainty = 1-controlled_iters/max(1,r_iter-1)
    else:
        uncertainty = 1
    return selected,query_time,rewires,max(set_curvature),uncertainty