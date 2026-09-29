import heapq
import math

# Hospital coordinates (same as Task 3)
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

# Hospital weighted graph
hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {},
}


def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def gbfs(start, goal, graph):
    frontier = [(heuristic(start, goal), start)]
    came_from = {start: None}
    expanded = []
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expanded.append(current)
        if current == goal:
            break
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    if goal not in came_from:
        return None, 0.0, expanded

    path = reconstruct_path(came_from, goal)
    total_cost = sum(graph[a][b] for a, b in zip(path, path[1:]))
    return path, total_cost, expanded


def a_star(start, goal, graph):
    frontier = [(heuristic(start, goal), start)]
    g_cost = {start: 0.0}
    came_from = {start: None}
    expanded = []
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expanded.append(current)
        if current == goal:
            break
        for neighbor, cost in graph[current].items():
            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_g + heuristic(neighbor, goal), neighbor))

    if goal not in g_cost:
        return None, 0.0, expanded

    path = reconstruct_path(came_from, goal)
    return path, g_cost[goal], expanded
