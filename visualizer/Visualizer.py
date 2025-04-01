## ----- Functions to Visualize the problem ---- ##
import matplotlib.pyplot as plt

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