##----- Algorithm to randomly create a coverage problem setting -----##
import numpy as np
from PoissonSampling import poisson_disk_sampling
from scipy.spatial import distance_matrix

# Auxiliary function: create random ellipsoid allocation points
def generate_ellipsoid_points(X, Y, R1, alpha, N):
    # Generate random points in a unit circle (polar coordinates)
    angles = np.random.uniform(0, 2*np.pi, N)  # Random angles
    radii = np.sqrt(np.random.uniform(0, 1, N))  # Uniform points inside circle
    # Convert to Cartesian coordinates
    x_unit = radii * np.cos(angles)
    y_unit = radii * np.sin(angles)   
    # Scale by alpha and R1 to create an ellipse
    x_ellipse = alpha * x_unit * R1
    y_ellipse = y_unit * R1  # y remains the same scaling as R1   
    # Translate to center (X, Y)
    x_final = x_ellipse + X
    y_final = y_ellipse + Y
    
    return np.column_stack((x_final, y_final))

# Main function:
def create_submodular_environment(num_points=5, num_targets=100, area_size=10, radius=2, overlapping=0.5, high_density_ratio=0.7):
    np.random.seed(42)  # For reproducibility
    target_points = []
    # Check the overlapping and compute how many nodes will be overlapped
    outliers = int((1-overlapping)*num_points); inliers = num_points - outliers 
    # Generate allocation points uniformly for the non-overlapped nodes
    uniform_points = np.random.rand(outliers, 2) * area_size
    # Generate allocation points for the overlapped zone usign Possion Point Processs
    poisson_points = poisson_disk_sampling(inliers, area_size, (1-overlapping)*radius)
    # Then, concat both
    allocation_points = np.vstack((uniform_points, poisson_points))
    np.random.shuffle(allocation_points)    
    # Split allocation points into high-density and low-density groups
    num_high_density = int(high_density_ratio * num_points)
    high_density_points = allocation_points[:num_high_density]  # More targets
    low_density_points = allocation_points[num_high_density:]   # Fewer targets    
    # Assign targets to high-density points (denser ellipsoids)
    for center in high_density_points:
        cluster_targets = generate_ellipsoid_points(center[0], center[1], radius, np.random.uniform(0.3, 1.7),
                                                    int(np.random.uniform(0.5*num_targets, num_targets)))
        target_points.extend(cluster_targets)
    # Assign targets to low-density points (sparser ellipsoids)
    low_density_targets = num_targets - len(target_points)
    for center in low_density_points:
        cluster_targets = generate_ellipsoid_points(center[0], center[1], radius, np.random.uniform(0.3, 1.7),
                                                    int(np.random.uniform(num_targets, 0.35*num_targets)))
        target_points.extend(cluster_targets)

    target_points = np.array(target_points)
    # Compute coverage matrix: Each allocation point covers targets within a given radius
    distances = distance_matrix(allocation_points, target_points)
    coverage_matrix = distances < radius  # Boolean matrix (num_points x num_targets)

    return allocation_points, target_points, radius
