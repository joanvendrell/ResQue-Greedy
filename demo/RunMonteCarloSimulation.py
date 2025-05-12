import numpy as np
import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from data.MonteCarlo import monte_carlo
from visualizer.Visualizer import plot_two_lines

def run_montecarlo(iterations, file_path1, file_path2):
    greedy_sol,resque_sol,random_sol,alan_sol,local_search_sol, instance_sol = monte_carlo(iterations)
    # Visualize N most different values:
    differences = np.abs(np.array(greedy_sol[0])-np.array(resque_sol[0]))
    indices = np.argsort(differences)[-100:]
    print(f"Total coverage for Greedy Algorithm: {sum(greedy_sol[0])/len(greedy_sol[0])}")
    print(f"Total coverage for ResQue-Greedy Algorithm: {sum(resque_sol[0])/len(resque_sol[0])}")
    print(f"Total coverage for Random Algorithm: {sum(random_sol[0])/len(random_sol[0])}")
    print(f"Total coverage for Modularity Algorithm: {sum(alan_sol[0])/len(alan_sol[0])}")
    print(f"Total coverage for Local Search Algorithm: {sum(local_search_sol[0])/len(local_search_sol[0])}")
    print(f"Total coverage for Instance Approximation Algorithm: {sum(instance_sol[0])/max(1,len(instance_sol[0]))}")
    print("------------------------------------------------------------------------")
    print(f"Total Time for Greedy Algorithm: {sum(greedy_sol[1])/len(greedy_sol[1])}")
    print(f"Total Time for ResQue-Greedy Algorithm: {sum(resque_sol[1])/len(resque_sol[1])}")
    print(f"Total Time for Random Algorithm: {sum(random_sol[1])/len(random_sol[1])}")
    print(f"Total Time for Modularity Algorithm: {sum(alan_sol[1])/len(alan_sol[1])}")
    print(f"Total coverage for Local Search Algorithm: {sum(local_search_sol[1])/len(local_search_sol[1])}")
    print(f"Total Time for Instance Approximation Algorithm: {sum(instance_sol[1])/len(instance_sol[1])}")
    print("------------------------------------------------------------------------")
    print(f"Total Queries for Greedy Algorithm: {sum(greedy_sol[2])/len(greedy_sol[2])}, using {sum(greedy_sol[3])/len(greedy_sol[3])} rewires")
    print(f"Total Queries for ResQue-Greedy Algorithm: {sum(resque_sol[2])/len(resque_sol[2])}, using {sum(resque_sol[3])/len(resque_sol[3])} rewires")
    print(f"Total Queries for Random Algorithm: {sum(random_sol[2])/len(random_sol[2])}, using {sum(random_sol[3])/len(random_sol[3])} rewires")
    print(f"Total Queries for Modularity Algorithm: {sum(alan_sol[2])/len(alan_sol[2])}, using {sum(alan_sol[3])/len(alan_sol[3])} rewires")
    print(f"Total Queries for Local Search Algorithm: {sum(local_search_sol[2])/len(local_search_sol[2])}")
    print("------------------------------------------------------------------------")
    print(f"Total Set Curvature for Greedy Algorithm: {sum(greedy_sol[4])/len(greedy_sol[4])}")
    print(f"Total Set Curvature for ResQue-Greedy Algorithm: {sum(resque_sol[4])/len(resque_sol[4])}")
    print(f"Total Set Curvature for Random Algorithm: {sum(random_sol[4])/len(random_sol[4])}")
    print(f"Total Set Curvature for Modularity Algorithm: {sum(alan_sol[4])/len(alan_sol[4])}")
    print("------------------------------------------------------------------------")
    print(f"Total Uncertainty for Greedy Algorithm: {sum(greedy_sol[5])/len(greedy_sol[5])}")
    print(f"Total Uncertainty for ResQue-Greedy Algorithm: {sum(resque_sol[5])/len(resque_sol[5])}")
    print(f"Total Uncertainty for Random Algorithm: {sum(random_sol[5])/len(random_sol[5])}")
    print(f"Total Uncertainty for Modularity Algorithm: {sum(alan_sol[5])/len(alan_sol[5])}")
    
    plot_two_lines(np.array(greedy_sol[0])[indices], np.array(resque_sol[0])[indices], np.array(random_sol[0])[indices], np.array(alan_sol[0])[indices], np.array(local_search_sol[0])[indices], np.array(instance_sol[0])[indices], True, file_path1)

    uniform_greedy = [greedy_sol[0][i]/max(local_search_sol[0][i],instance_sol[0][i]) for i in range(len(greedy_sol[0]))]
    uniform_resque = [resque_sol[0][i]/max(local_search_sol[0][i],instance_sol[0][i]) for i in range(len(resque_sol[0]))]
    uniform_random = [random_sol[0][i]/max(local_search_sol[0][i],instance_sol[0][i]) for i in range(len(random_sol[0]))]
    uniform_alan = [alan_sol[0][i]/max(local_search_sol[0][i],instance_sol[0][i]) for i in range(len(alan_sol[0]))]
    uniform_local = [local_search_sol[0][i]/max(local_search_sol[0][i],instance_sol[0][i]) for i in range(len(local_search_sol[0]))]
    uniform_instance = [instance_sol[0][i]/max(local_search_sol[0][i],instance_sol[0][i]) for i in range(len(local_search_sol[0]))]
    plot_two_lines(np.array(uniform_greedy)[indices], np.array(uniform_resque)[indices], np.array(uniform_random)[indices], [], np.array(uniform_local)[indices], np.array(uniform_instance)[indices], True, file_path2)


if __name__ == "__main__":
    # Argument Parser
    parser = argparse.ArgumentParser(description='Run reachability experiments')
    parser.add_argument('--iterations', type=str, required=True, help='Dataset')
    parser.add_argument('--file_path1', type=str, required=True, help='First plot')
    parser.add_argument('--file_path2', type=str, required=True, help='Second plot')
    args = parser.parse_args()
    
    run_reachability_experiments(args.iterations,args.file_path1,args.file_path2)