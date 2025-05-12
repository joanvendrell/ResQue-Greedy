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
import argparse
from scipy.spatial import distance_matrix
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from auxiliary.Auxiliary import get_combinations, prepare_probabilistic_reachability_sets
from auxiliary.InstanceApproximation import OPT_submodular_upper_bound_reachability
from auxiliary.LocalSearch import local_search_submodular_maximization_reachability
from main.ResQueGreedy import greedy_reachability

def run_reachability_experiments(dataset,k,rewiring_limit,seed,num_workers,tau):
    # Select Dataset
    if dataset == "twitch":
        with open("../data/data/twitch_graph_ES.pkl", "rb") as f:
            G = pickle.load(f)
        with open("../data/data_processed/reachability_twitch_1000_10.json", "r") as f:
            reachability_dict = json.load(f)
    elif dataset == "youtube":
        with open("../data/data/youtube_graph.pkl", "rb") as f:
            G = pickle.load(f)
        with open("../data/data_processed/reachability_youtube_1000_40.json", "r") as f:
            reachability_dict = json.load(f)
    elif dataset == "arxiv":
        with open("../data/data/arxiv_graph.pkl", "rb") as f:
            G = pickle.load(f)
        with open("../data/data_processed/reachability_arxiv_1000_60.json", "r") as f:
            reachability_dict = json.load(f)
    elif dataset == "caltech_facebook":
        with open("../data/data/cal_tech_facebook_graph.pkl", "rb") as f:
            G = pickle.load(f)
        with open("../data/data_processed/reachability_caltechfacebook_1000_80.json", "r") as f:
            reachability_dict = json.load(f)
    # Instance Approximation:
    start_time = time.time()
    opt = OPT_submodular_upper_bound_reachability(G, reachability_dict, seed, num_workers, k)
    duration = time.time() - start_time
    print("--------------------- Instance Approximation ---------------------\n")
    print(f"The Instance Approximation is {opt}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    
    # Greedy Algorithm:
    start_time = time.time()
    selected_greedy,queries,rewires,set_curvature,uncertainty = greedy_reachability(G, reachability_dict, k)
    duration = time.time() - start_time
    print("--------------------- Greedy ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    reached_targets = prepare_probabilistic_reachability_sets(G, reachability_dict, selected_greedy, seed)
    print(f"Total coverage for {k} selected points: {reached_targets}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {reached_targets/opt}\n")
    
    # Local Search:
    start_time = time.time()
    S,f_opt,query_time, results = local_search_submodular_maximization_reachability(G, reachability_dict, k, seed, selected_greedy, 1e-5, 100)
    duration = time.time() - start_time
    print("--------------------- Local Search ---------------------\n")
    print(f"The Local Search is {f_opt}\n")
    print(f"Total time for {k} selected points: {duration/k} with {query_time} queries.\n")
    print(f"The instance ratio is {f_opt/opt}\n")
    
    # Classical ResQue:
    start_time = time.time()
    selected_greedy,queries,rewires,set_curvature,uncertainty = greedy_reachability(G, reachability_dict, k, "ResQue", rewiring_limit, num_workers=num_workers)
    duration = time.time() - start_time
    print("--------------------- ResQue ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    reached_targets = prepare_probabilistic_reachability_sets(G, reachability_dict, selected_greedy, seed)
    print(f"Total coverage for {k} selected points: {reached_targets}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {reached_targets/opt}\n")
    
    # Modularity ResQue:
    start_time = time.time()
    selected_greedy,queries,rewires,set_curvature,uncertainty = greedy_reachability(G, reachability_dict, k, "Modularity", rewiring_limit, num_workers=num_workers, tau=0.8)
    duration = time.time() - start_time
    print("--------------------- Modularity ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    reached_targets = prepare_probabilistic_reachability_sets(G, reachability_dict, selected_greedy, seed)
    print(f"Total coverage for {k} selected points: {reached_targets}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {reached_targets/opt}\n")
    
    # Probabilistic ResQue:
    start_time = time.time()
    selected_greedy,queries,rewires,set_curvature,uncertainty = greedy_reachability(G, reachability_dict, k, "Probabilistic", rewiring_limit, num_workers=num_workers)
    duration = time.time() - start_time
    print("--------------------- Probabilistic ---------------------\n")
    print("Selected >> ",selected_greedy,"\n")
    reached_targets = prepare_probabilistic_reachability_sets(G, reachability_dict, selected_greedy, seed)
    print(f"Total coverage for {k} selected points: {reached_targets}\n")
    print(f"Total time for {k} selected points: {duration/k}\n")
    print(f"Total queries for {k} selected points: {queries}\n")
    print(f"Total uncertainty for {k} selected points: {uncertainty}\n")
    print(f"The instance ratio is {reached_targets/opt}\n")

if __name__ == "__main__":
    # "Usage: python3 run_reachability_experiments.py <dataset> <k> <rewiring_limit> <seed> <num_workers> <tau>")
    # Argument Parser
    parser = argparse.ArgumentParser(description='Run reachability experiments')
    parser.add_argument('--dataset', type=str, required=True, help='Dataset')
    parser.add_argument('--k', type=int, default=10, help='Number of selected points')
    parser.add_argument('--rewiring_limit', type=float, default=5, help='Rewiring limit')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--num_workers', type=int, default=5, help='Number of parallel workers')
    parser.add_argument('--tau', type=int, default=0.5, help='Threshold on faulty detection')
    args = parser.parse_args()
    
    run_reachability_experiments(args.dataset,args.k,args.rewiring_limit,args.seed,args.num_workers,args.tau)