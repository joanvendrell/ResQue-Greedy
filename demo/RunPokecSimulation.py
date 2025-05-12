import os
import urllib.request
import gzip
import time
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
import os
from scipy.spatial import distance_matrix
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from auxiliary.Auxiliary import get_combinations, compute_coverage
from main.ResQueGreedy import greedy_coverage
from auxiliary.InstanceApproximation import OPT_submodular_upper_bound_coverage
from auxiliary.LocalSearch import local_search_submodular_maximization_coverage

def run_coverage_experiments(k,rewiring_limit,tau):
    #Import data
    with open('../data/data/pokec_coverage.pkl', 'rb') as f:
        coverage_dict = pickle.load(f)
    
    start_time = time.time()
    opt = OPT_submodular_upper_bound_coverage(coverage_dict, k)
    duration = time.time() - start_time
    print("--------------------- Instance Approximation ---------------------\n")
    print(f"The Instance Approximation is {opt}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    
    start_time = time.time()
    selected_greedy,queries,rewires,set_curvature,uncertainty = greedy_coverage([],coverage_dict, k)
    duration = time.time() - start_time
    #plot_environment(allocation_points, target_points, radius, selected)
    print("--------------------- Greedy ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    print(f"Total coverage for {k} selected points: {len(compute_coverage(coverage_dict,selected_greedy))}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {len(compute_coverage(coverage_dict,selected_greedy))/opt}\n")
    
    start_time = time.time()
    selected_resque,queries,rewires,set_curvature,uncertainty = greedy_coverage([],coverage_dict, k, "ResQue", rewiring_limit)
    duration = time.time() - start_time
    #plot_environment(allocation_points, target_points, radius, selected)
    print("--------------------- ResQue ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    print(f"Total coverage for {k} selected points: {len(compute_coverage(coverage_dict,selected_resque))}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {len(compute_coverage(coverage_dict,selected_resque))/opt}\n")
    
    start_time = time.time()
    selected_resque,queries,rewires,set_curvature,uncertainty = greedy_coverage([],coverage_dict, k, "Modularity", rewiring_limit)
    duration = time.time() - start_time
    #plot_environment(allocation_points, target_points, radius, selected)
    print("--------------------- Modularity ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    print(f"Total coverage for {k} selected points: {len(compute_coverage(coverage_dict,selected_resque))}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {len(compute_coverage(coverage_dict,selected_resque))/opt}\n")
    
    start_time = time.time()
    selected_resque,queries,rewires,set_curvature,uncertainty = greedy_coverage([],coverage_dict, k, "Probabilistic", rewiring_limit)
    duration = time.time() - start_time
    #plot_environment(allocation_points, target_points, radius, selected)
    print("--------------------- Probabilistic ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    print(f"Total coverage for {k} selected points: {len(compute_coverage(coverage_dict,selected_resque))}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {len(compute_coverage(coverage_dict,selected_resque))/opt}\n")
    
    start_time = time.time()
    S,f_opt,queries = local_search_submodular_maximization_coverage(coverage_dict, k, selected_greedy, epsilon=1e-5, max_iters=100)
    duration = time.time() - start_time
    print("--------------------- Local Search ---------------------\n")
    print(f"The Local Search is {f_opt}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"The instance ratio is {f_opt/opt}\n")

if __name__ == "__main__":
    # "Usage: python run_coverage_experiments.py <k> <rewiring_limit> <tau>")
    # Argument Parser
    parser = argparse.ArgumentParser(description='Run reachability experiments')
    parser.add_argument('--k', type=int, default=50, help='Number of selected points')
    parser.add_argument('--rewiring_limit', type=float, default=5, help='Rewiring limit')
    parser.add_argument('--tau', type=int, default=0.5, help='Threshold on faulty detection')
    args = parser.parse_args()
    
    run_coverage_experiments(args.k,args.rewiring_limit,args.tau)