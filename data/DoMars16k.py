## ----- DoMars16k ----- ##

import os
import re
import random
from collections import defaultdict

# Auxiliary function to observe the features map
def count_image_keys(base_folder: str) -> dict:
    # Initialize a dictionary to store counts
    counts = defaultdict(int)
    # Define the main subdirectories
    subdirs = ['train', 'test', 'val']
    # Traverse through the subdirectories
    for subdir in subdirs:
        folder_path = os.path.join(base_folder, subdir)
        # Traverse all folders and files within the subdirectory
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                # Check if the file has the expected naming pattern
                if file_name.count('_') >= 4:
                    # Split the file name and extract the key
                    key = file_name.split('_')[4]
                    # Increment the count for this key
                    counts[key] += 1
    return dict(counts)

# Auxiliary function to observe the features map
def split_numbers_and_letters(input_string):
    # Use regular expression to find all numbers and letters
    numbers = re.findall(r'\d+', input_string)  # Find all numeric sequences
    letters = re.findall(r'[A-Za-z]', input_string)  # Find all individual letters
    
    # Return both lists
    return numbers, letters
        
# Function to generate random points within a circular range
def generate_random_points(data: dict, r: float) -> list:
    points = []; centers = []
    for key, value in data.items():
        numbers, letters = split_numbers_and_letters(key)
        # Parse the latitude and longitude from the key
        lat = int(numbers[0]) * (-1 if 'S'==letters[0] else 1)
        lon = int(numbers[1]) * (1 if 'W'==letters[1] else -1)
        center = (lon, lat)
        centers.append(center)
        # Generate random points around the center
        for _ in range(value):
            points.append((random.uniform(center[0], center[0] + r), random.uniform(center[1], center[1] + r)))
    return points, centers