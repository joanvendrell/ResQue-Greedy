## ----- Functions to Visualize the problem ---- ##
import matplotlib.pyplot as plt

# Function to plot the coverage problem
def plot_environment(allocation_points, target_points, radius, selected=None):
    plt.figure(figsize=(8, 8))
    plt.scatter(target_points[:, 0], target_points[:, 1], c='blue', s=20, label='Target Points')
    plt.scatter(allocation_points[:, 0], allocation_points[:, 1], c='black', s=100, label='Allocation Points')
    if selected is not None:
        for idx in selected:
            circle = plt.Circle(allocation_points[idx], radius, color='red', fill=False, linewidth=2)
            plt.gca().add_patch(circle)
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    #plt.legend()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.grid()
    plt.show()

# Function to plot two lists as independent lines over the same x-axis
def plot_two_lines(y_g, y_rw_g, y_e, c_rw_g):
    plt.figure(figsize=(12, 10))
    x = list(range(len(y_rw_g)))
    plt.plot(x, y_g, label="Greedy Algorithm", marker='o')
    plt.plot(x, y_rw_g, label="ResQue Greedy Algorithm", marker='s')
    plt.plot(x, y_e, label="Random Re-Wiring Algorithm", marker='x')
    plt.ylabel('Return')
    #plt.plot(x, [y_g[i]/(1-c_rw_g[i]) for i in range(len(y_g))], label="New Curvature bound", marker='*')
    #plt.plot(x, [y_g[i]/(1-np.exp(-1)) for i in range(len(y_g))], label="Classical Curvature bound", marker='D')
    #plot the bounds
    plt.legend(loc='upper left',fontsize=16)
    plt.xticks(fontsize=16)  # Change the x-axis tick label size
    plt.yticks(fontsize=16) 
    plt.grid(True)
    plt.show()
