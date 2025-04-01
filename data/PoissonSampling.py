##----- Algorithm to run a Poisson Sampling (DPP) to define submodular environments ------##
import random
import numpy as np

# Auxiliary function: Convert a point to grid index
def point_to_grid(p,cell_size):
    return int(p[0] / cell_size), int(p[1] / cell_size)

# Poisson Disk Sampling:  N -- number of points
#                         A -- area
#                         r -- radius
#                         k -- candidates to try at each iteration

def poisson_disk_sampling(N, A, r, k=30):
    cell_size = r / np.sqrt(2)  # Grid cell size
    grid_size = int(A / cell_size) + 1  # Grid dimensions
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    # Initial point
    first_point = np.random.rand(2) * A
    active_list = [first_point]
    points = [first_point]
    # Place first point in grid
    gx, gy = point_to_grid(first_point,cell_size)
    grid[gx][gy] = first_point
    # Start sampling
    while active_list and len(points) < N:
        idx = random.randint(0, len(active_list) - 1)
        center = active_list[idx]
        found = False
        
        for _ in range(k):  # Try k candidates around center
            angle = random.uniform(0, 2 * np.pi)
            radius = random.uniform(r, 2 * r)
            
            new_point = center + radius * np.array([np.cos(angle), np.sin(angle)])
            
            # Check if within bounds
            if not (0 <= new_point[0] <= A and 0 <= new_point[1] <= A):
                continue
            
            # Check minimum distance
            gx, gy = point_to_grid(new_point,cell_size)
            neighbors = [
                grid[i][j] for i in range(max(0, gx-2), min(grid_size, gx+3))
                for j in range(max(0, gy-2), min(grid_size, gy+3)) if grid[i][j] is not None
            ]
            if all(np.linalg.norm(new_point - np.array(p)) >= r for p in neighbors):
                points.append(new_point)
                active_list.append(new_point)
                grid[gx][gy] = new_point
                found = True
                break
        
        if not found:
            active_list.pop(idx)  # Remove from active list if no new points
    
    return np.array(points[:N])  # Ensure we return exactly N points