## ----- Functions to Visualize the problem ---- ##
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../data/data/')))

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
def plot_two_lines(greedy, resque, random_rew, alan, local, instance, save=False, save_path="plot.png"):
    plt.figure(figsize=(12, 10))
    x = list(range(len(resque)))
    if len(greedy):
        plt.plot(x, greedy, label="Greedy Algorithm", marker='o')
    if len(resque):
        plt.plot(x, resque, label="ResQue Greedy Algorithm", marker='s')
    if len(random_rew):
        plt.plot(x, random_rew, label="Random Rewiring Algorithm", marker='x')
    if len(alan):
        plt.plot(x, alan, label="Modularity ResQue Algorithm", marker='^')
    if len(local):
        plt.plot(x, local, label="Local Search Algorithm", marker='*')
    if len(instance):
        plt.plot(x, instance, label="Instance Approximation Algorithm", marker='+')
    plt.ylabel('Return')
    #plot the bounds
    plt.legend(loc='lower left',fontsize=16)
    plt.xticks(fontsize=16)  # Change the x-axis tick label size
    plt.yticks(fontsize=16) 
    plt.grid(True)
    if save:
        plt.savefig(output_file, format='png', dpi=300)
        print(f"Plot saved as {output_file}")
    plt.show()

# Function to plot a vector
def vector_plot(v,name="Vector Plot"):
    plt.figure()
    plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1)
    plt.xlim(-1, 4)
    plt.ylim(-1, 4)
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(name)
    plt.show()

# Function to plot allocation points and random points over Mars Map
def plot_points(random_points, centers, greedy=None, resque=None, random=None):
    plt.figure(figsize=(20, 12))
    img = mpimg.imread("../data/data/map-mars.jpg")
    plt.imshow(img, extent=[-160, 210, -90, 100], alpha=0.8)
    for point in random_points:
        plt.scatter(point[0]-160, point[1], s=10, color='blue', alpha=0.6)
    for point in centers:
        plt.scatter(point[0]-160, point[1], s=500, color='black', alpha=0.6,marker='*')
    # V line
    plt.axvline(x=-150, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=-120, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=-90, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=-60, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=-30, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=0, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=30, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=60, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=90, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=120, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=150, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axvline(x=180, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    # H line
    plt.axhline(y=-90, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axhline(y=-60, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axhline(y=-30, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axhline(y=30, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axhline(y=60, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    plt.axhline(y=90, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0
    #plt.xlabel('Longitude')
    #plt.ylabel('Latitude')
    #plt.title('Allocation Points and Randomly Distributed Points')
    #plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1)) 
    #plt.axis('equal')
    #plt.grid(True)
    for e in greedy:
        x,y = centers[e]  # Get coordinates
        circle = plt.Circle((x-160, y), radius=10, color='blue', fill=False, linewidth=2)
        plt.gca().add_patch(circle)
    for e in resque:
        x,y = centers[e]  # Get coordinates
        circle = plt.Circle((x-160, y), radius=11, color='orange', fill=False, linewidth=2)
        plt.gca().add_patch(circle)
    for e in random:
        x,y = centers[e]  # Get coordinates
        circle = plt.Circle((x-160, y), radius=9, color='green', fill=False, linewidth=2)
        plt.gca().add_patch(circle)
    plt.show()
