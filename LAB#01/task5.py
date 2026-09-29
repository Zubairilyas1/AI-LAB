# Task 5: Intelligent Public Transport Route Analyzer (Beginner Version)
# AI-2002 Lab

import numpy as np
import math

# ---------- Part A: Route Representation ----------
# 1. Tuples for coordinates (already given)
stops = [
    ("Stop A", (33.6425, 73.1730)),
    ("Stop B", (33.6500, 73.1600)),
    ("Stop C", (33.6550, 73.1500)),
    ("Stop D", (33.6600, 73.1400)),
    ("Stop E", (33.6650, 73.1300))
]

# 2. Dictionary mapping stop name to coordinates
stop_coords = {}
for stop_name, coords in stops:
    stop_coords[stop_name] = coords

print("=== Part A: Route Representation ===")
print("Stop coordinates dictionary:")
for name, coords in stop_coords.items():
    print(" ", name, "→", coords)
print("\n")

# ---------- Part B: Route Exploration ----------
# 3. Set to maintain visited stops
visited_stops = set()

# 4. Function to check if a stop is visited
def is_visited(stop_name):
    return stop_name in visited_stops

# 5. Function to add a stop to visited set
def add_visited(stop_name):
    visited_stops.add(stop_name)

# Example: we'll add stops as we process the route later

# ---------- Part C: Nested Route Processing ----------
# 6. Recursive function to flatten nested routes
routes = [
    ["Stop A", "Stop B", ["Stop C", "Stop D"]],
    ["Stop A", ["Stop E"]]
]

def flatten_route(route_list):
    flat = []
    for item in route_list:
        if isinstance(item, list):
            # If item is a list, recursively flatten it
            flat = flat + flatten_route(item)
        else:
            # It's a stop name (string)
            flat.append(item)
    return flat

# Flatten the entire routes list (which is a list of lists)
flat_route = flatten_route(routes)

print("=== Part C: Flattened Route ===")
print("Flat route:", flat_route)
print("\n")

# Now add each stop in the flattened route to visited set
for stop in flat_route:
    add_visited(stop)

# ---------- Part D: Distance Calculation ----------
# 7. Function to calculate Euclidean distance between two (lat, lon) points
def calculate_distance(point1, point2):
    lat1, lon1 = point1
    lat2, lon2 = point2
    # Euclidean distance in degrees (simplified)
    distance = math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    return distance

# We'll use this later to compute distances between consecutive stops

# ---------- Part E: NumPy Analysis ----------
# 8. Store coordinates in a NumPy array
coords_list = [stop_coords[stop] for stop in stop_coords]  # we want them in order of stops list
# Actually we need all stops in order of the list "stops" to preserve the order
# But we have the original stops list with names and coords in order.
# Let's extract coordinates in that order:
coords_array = np.array([coords for _, coords in stops])

print("=== Part E: NumPy Analysis ===")
print("Coordinates array:")
print(coords_array)
print("\n")

# 9. Calculate mean, min, max of latitude and longitude
# Latitude is column 0, Longitude is column 1
mean_lat = np.mean(coords_array[:, 0])
mean_lon = np.mean(coords_array[:, 1])
min_lat = np.min(coords_array[:, 0])
max_lat = np.max(coords_array[:, 0])

print("Mean latitude:", mean_lat)
print("Mean longitude:", mean_lon)
print("Minimum latitude:", min_lat)
print("Maximum latitude:", max_lat)
print("\n")

# 10. Calculate distance between consecutive stops
# We'll use the original order of stops
distances = []
for i in range(len(stops) - 1):
    point1 = stops[i][1]   # coordinates of stop i
    point2 = stops[i+1][1] # coordinates of stop i+1
    dist = calculate_distance(point1, point2)
    distances.append(dist)
    print("Distance between", stops[i][0], "and", stops[i+1][0], ":", round(dist, 6))

print("\n")

# ---------- Part F: Route Decision ----------
# 11. Identify the closest pair of consecutive stops
if distances:
    min_dist = min(distances)
    min_index = distances.index(min_dist)
    closest_pair = (stops[min_index][0], stops[min_index+1][0])
    print("Closest pair of consecutive stops:", closest_pair[0], "and", closest_pair[1], 
          "with distance:", round(min_dist, 6))
else:
    print("No consecutive stops to compare.")

print("\n")

# 12. Display the complete flattened route (already done, but we'll show again)
print("Complete flattened route:", flat_route)

# 13. Display the visited stops
print("Visited stops:", visited_stops)

# 14. Display calculated route statistics
print("\n=== Part F: Route Statistics ===")
print("Total number of stops:", len(stops))
print("Total distinct stops visited:", len(visited_stops))
print("Number of route segments (edges):", len(distances))
if distances:
    print("Total route length (sum of distances):", round(sum(distances), 6))
    print("Average segment distance:", round(sum(distances)/len(distances), 6))
    print("Minimum segment distance:", round(min(distances), 6))
    print("Maximum segment distance:", round(max(distances), 6))

# Extra: Print the route in a nice way with arrows
print("\nRoute path:")
for i, stop in enumerate(flat_route):
    if i == len(flat_route)-1:
        print(stop)
    else:
        print(stop, "→ ", end="")

print("\n")
print("="*50)
print("          END OF ANALYSIS")
print("="*50)