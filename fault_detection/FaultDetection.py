## ------- Fault-Detection Mechanism ----- ##
import numpy as np
from Auxiliary import get_combinations
import random

# Fault-detection mechaism
def fault_detection(selected,trace_curvature,curvatures,strategy):
    if strategy == "ResQue":
        z = np.random.rand(1)
        gamma = max(max(trace_curvature,default=0),max(curvatures,default=0))
        if z <= gamma/(1+gamma):
            return True
    elif strategy == "Random":
        z1 = np.random.rand(1); z2 = np.random.rand(1)
        if z1 >= z2:
            return True
    return False

# Re-wiring strategy
def rewiring(groundset,selected,trace_curvature,strategy):
    if strategy == "ResQue":
        differences = [abs(trace_curvature[i] - trace_curvature[i-1]) for i in range(1, len(trace_curvature))]
        if not differences:
            return selected, trace_curvature
        element = selected[differences.index(max(differences))]
        selected.remove(element)
        trace_curvature.remove(trace_curvature[differences.index(max(differences))])
        return selected, trace_curvature
    elif strategy == "Random":
        options = get_combinations(groundset, len(selected))
        return list(random.choice(options)), trace_curvature