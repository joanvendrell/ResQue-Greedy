## ----- MonteCarlo Simulator ----- ##
import numpy as np
from tqdm import tqdm
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from data.RandomCoverageSetting import create_submodular_environment
from auxiliary.Auxiliary import compute_coverage
from main.ResQueGreedy import greedy_coverage
from auxiliary.InstanceApproximation import OPT_submodular_upper_bound_coverage
from auxiliary.LocalSearch import local_search_submodular_maximization_coverage

def monte_carlo(num_experiments):
    # Collectors
    instance_return, instance_time = [],[]
    greedy_return, greedy_time, greedy_query, greedy_rewires, greedy_set_curvature, greedy_uncertain = [],[],[],[],[],[]
    rw_greedy_return, rw_greedy_time, rw_greedy_query, rw_greedy_rewires, rw_set_curvature, rw_uncertain = [],[],[],[],[],[]
    random_greedy_return,random_greedy_time,random_greedy_query,random_greedy_rewires,random_set_curvature,random_uncertain=[],[],[],[],[],[]
    a_greedy_return, a_greedy_time, a_greedy_query, a_greedy_rewires, a_set_curvature, a_uncertain = [],[],[],[],[],[]
    local_greedy_return, local_greedy_time, local_greedy_query = [],[],[]
    # Initiate experiment
    for _ in tqdm(range(num_experiments)):
        # generate random environments
        num_points = np.random.randint(10, 30) 
        num_targets = np.random.randint(num_points * 10, num_points * 50)
        area_size = np.random.randint(5, 20) 
        radius = np.random.uniform(1, area_size / 5) 
        k = np.random.randint(1, num_points)  
        overlapping = np.random.uniform(0.6,0.9)
        high_density_ratio = np.random.uniform(0.4,0.8)
        allocation_points, ground_set, input_data = create_submodular_environment(num_points, num_targets, area_size, 
                                                                                     radius, overlapping, high_density_ratio)
        # instance approximation
        start_time = time.time()
        opt = OPT_submodular_upper_bound_coverage(input_data, k)
        instance_return.append(opt)
        instance_time.append(time.time() - start_time)
        
        # run greedy algorithm
        start_time = time.time()
        selected_greedy,queries,rewires,set_curvature,uncertainty = greedy_coverage(ground_set,input_data, k)
        coverage = len(compute_coverage(input_data,selected_greedy))
        greedy_time.append(time.time() - start_time)
        greedy_return.append(coverage)
        greedy_query.append(queries)
        greedy_rewires.append(rewires)
        greedy_set_curvature.append(set_curvature)
        greedy_uncertain.append(uncertainty)

        # run curvature-averse re-wiring greedy algorithm
        start_time = time.time()
        selected,queries,rewires,set_curvature,uncertainty = greedy_coverage(ground_set,input_data, k, "ResQue", 5) 
        coverage = len(compute_coverage(input_data,selected))
        rw_greedy_time.append(time.time() - start_time)
        rw_greedy_return.append(coverage)
        rw_greedy_query.append(queries)
        rw_greedy_rewires.append(rewires)
        rw_set_curvature.append(set_curvature)
        rw_uncertain.append(uncertainty)

        # run random curvature-averse greedy algorithm
        start_time = time.time()
        selected,queries,rewires,set_curvature,uncertainty = greedy_coverage(ground_set,input_data, k, "Random", 4) 
        coverage = len(compute_coverage(input_data,selected))
        random_greedy_time.append(time.time() - start_time)
        random_greedy_return.append(coverage)
        random_greedy_query.append(queries)
        random_greedy_rewires.append(rewires)
        random_set_curvature.append(set_curvature)
        random_uncertain.append(uncertainty)

        # run random curvature-averse greedy algorithm
        start_time = time.time()
        selected,queries,rewires,set_curvature,uncertainty = greedy_coverage(ground_set,input_data, k, "Modularity", 4) 
        coverage = len(compute_coverage(input_data,selected))
        a_greedy_time.append(time.time() - start_time)
        a_greedy_return.append(coverage)
        a_greedy_query.append(queries)
        a_greedy_rewires.append(rewires)
        a_set_curvature.append(set_curvature)
        a_uncertain.append(uncertainty)

        # local search algorithm
        start_time = time.time()
        S,f_opt,queries,results = local_search_submodular_maximization_coverage(input_data, k, selected_greedy, epsilon=1e-5, max_iters=100)
        local_greedy_time.append(time.time() - start_time)
        local_greedy_return.append(f_opt)
        local_greedy_query.append(queries)
        
    return  [greedy_return, greedy_time, greedy_query, greedy_rewires, greedy_set_curvature, greedy_uncertain],[rw_greedy_return, rw_greedy_time, rw_greedy_query, rw_greedy_rewires, rw_set_curvature, rw_uncertain],[random_greedy_return, random_greedy_time, random_greedy_query, random_greedy_rewires, random_set_curvature, random_uncertain], [a_greedy_return, a_greedy_time, a_greedy_query, a_greedy_rewires, a_set_curvature, a_uncertain], [local_greedy_return, local_greedy_time, local_greedy_query], [instance_return, instance_time]

