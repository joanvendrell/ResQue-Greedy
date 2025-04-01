## ----- MonteCarlo Simulator ----- ##
import numpy as np
from RandomCoverageSetting import create_submodular_environment
from Auxiliary import compute_coverage
from ResQueGreedy import greedy_coverage
import time
def monte_carlo(num_experiments):
    # Collectors
    greedy_return, greedy_time, greedy_query, greedy_rewires, greedy_set_curvature = [],[],[],[],[]
    rw_greedy_return, rw_greedy_time, rw_greedy_query, rw_greedy_rewires, rw_set_curvature = [],[],[],[],[]
    random_greedy_return, random_greedy_time, random_greedy_query, random_greedy_rewires, random_set_curvature = [],[],[],[],[]
    # Initiate experiment
    for _ in tqdm(range(num_experiments)):
        #print(f"Iteration X:")
        # generate random environments
        num_points = np.random.randint(10, 30) 
        num_targets = np.random.randint(num_points * 10, num_points * 50) #np.random.randint(num_points * 10, num_points * 50)  
        area_size = np.random.randint(5, 20)  #np.random.randint(5, 20)  
        radius = np.random.uniform(1, area_size / 5) #np.random.uniform(1, area_size / 5)  
        k = np.random.randint(1, num_points)  
        overlapping = np.random.uniform(0.6,0.9)
        high_density_ratio = np.random.uniform(0.4,0.8)
        allocation_points, target_points, radius = create_submodular_environment(num_points, num_targets, area_size, 
                                                                                 radius, overlapping, high_density_ratio)
        #print(">> Run Greedy...")
        # run greedy algorithm
        start_time = time.time()
        selected,queries,rewires,trace_curvature = greedy_coverage(allocation_points, target_points, radius, k)
        coverage = len(compute_coverage(allocation_points[selected], target_points, radius))
        greedy_time.append(time.time() - start_time)
        greedy_return.append(coverage)
        greedy_query.append(queries)
        greedy_rewires.append(rewires)
        greedy_set_curvature.append(max(trace_curvature))
        #print(">> Run ResQue...")
        # run curvature-averse re-wiring greedy algorithm
        start_time = time.time()
        selected,queries,rewires,trace_curvature = greedy_coverage(allocation_points, target_points, radius, k, "ResQue") 
        coverage = len(compute_coverage(allocation_points[selected], target_points, radius))
        rw_greedy_time.append(time.time() - start_time)
        rw_greedy_return.append(coverage)
        rw_greedy_query.append(queries)
        rw_greedy_rewires.append(rewires)
        rw_set_curvature.append(max(trace_curvature))
        #print(">> Run Random...")
        # run random curvature-averse greedy algorithm
        start_time = time.time()
        selected,queries,rewires,trace_curvature = greedy_coverage(allocation_points, target_points, radius, k, "Random") 
        coverage = len(compute_coverage(allocation_points[selected], target_points, radius))
        random_greedy_time.append(time.time() - start_time)
        random_greedy_return.append(coverage)
        random_greedy_query.append(queries)
        random_greedy_rewires.append(rewires)
        random_set_curvature.append(max(trace_curvature))
        
    return  [greedy_return, greedy_time, greedy_query, greedy_rewires, greedy_set_curvature],
            [rw_greedy_return, rw_greedy_time, rw_greedy_query, rw_greedy_rewires, rw_set_curvature],
            [random_greedy_return, random_greedy_time, random_greedy_query, random_greedy_rewires, random_set_curvature]

