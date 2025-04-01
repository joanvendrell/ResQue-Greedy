## ----- Functions to Visualize the problem ---- ##
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

# Function to plot allocation points and random points over Mars Map
def plot_points(random_points, centers, greedy=None, resque=None, random=None):
    plt.figure(figsize=(20, 12))
    img = mpimg.imread('map-mars.jpg')
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
