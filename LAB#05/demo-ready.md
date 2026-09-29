# Week 5 Demo: Uninformed Search Strategies (BFS, DFS, UCS)

**Course:** Artificial Intelligence | **Lab:** Week 5 | **CLO-2:** Apply classical AI techniques to solve structured problems

---

## Quick Reference: What Each Algorithm Does

| Feature | BFS | DFS | UCS |
|---------|-----|-----|-----|
| **Data Structure** | Queue (FIFO) | Stack (LIFO) | Priority Queue (heapq) |
| **Explores** | Level by level | Deep first, then backtracks | Lowest cost first |
| **Optimal for** | Fewest edges (unweighted) | Not guaranteed | Lowest total cost (weighted) |
| **Complete?** | Yes (finite graph) | Yes (with visited set) | Yes (non-negative costs) |
| **Memory** | High (stores entire level) | Low (stores current path) | Moderate |
| **Real-world use** | Minimum transfers | File system search | Route planning |

---

## TASK 1: BFS for Minimum-Transfer Public Transport Routing

### What It Does
Finds the route with **minimum number of transfers** from FAST University to PIMS Metro Station using Islamabad's transport network.

### Key Answer Points

**Q: Why BFS and not DFS?**
> BFS guarantees the shortest path in an **unweighted graph** (minimum edges). Since every transfer is one equal-cost transition, BFS finds the minimum-transfer route. DFS might find a longer route first because it goes deep into one branch.

**Q: Why test goal when popping from queue, not when pushing?**
> If we test when pushing, we might find the goal via a longer path first (if it's added early). Testing when popping guarantees we've explored ALL nodes at the current level first — so the first time we pop the goal, it's at the **minimum depth**.

**Q: What is the role of the visited set?**
> Prevents cycles (e.g., NUST ↔ G-11 ↔ H-8 ↔ FAST) and prevents re-adding nodes already in the queue. Without it, BFS would loop infinitely on cyclic graphs.

**Q: Why use `deque` instead of a regular list?**
> `deque.popleft()` is O(1), while `list.pop(0)` is O(n). BFS constantly removes from the front, so `deque` is efficient.

**Q: What does the `parent` dictionary do?**
> Stores `child → parent` mapping. After finding the goal, we walk backwards from goal to start using parent pointers to reconstruct the path. This is O(V) space instead of storing full paths.

**Q: What does `level` track?**
> `level[node] = distance from start in edges`. `level[neighbor] = level[current] + 1`. This shows BFS explores level 0 → 1 → 2 → 3.

### Graph Structure
```
FAST University → NUST Metro Station → Faiz Ahmed Faiz Metro Station → PIMS (3 transitions)
FAST University → G-11 Metro Station (alternative)
FAST University → H-8 Metro Station → I-8 → Blue Area → PIMS (longer alternative)
NUST → Saddar → Faiz Ahmed Faiz (alternative branch)
```

### Actual Output
```
Traversal Order:
  1. FAST University
  2. NUST Metro Station
  3. G-11 Metro Station
  4. H-8 Metro Station
  5. Faiz Ahmed Faiz Metro Station
  6. Saddar Metro Station
  7. I-8 Metro Station
  8. PIMS Metro Station

Solution Path:
FAST University → NUST Metro Station → Faiz Ahmed Faiz Metro Station → PIMS Metro Station

Number of Transitions: 3
```

### Why BFS Explores Level by Level
- **Level 0:** FAST University
- **Level 1:** NUST, G-11, H-8 (directly connected)
- **Level 2:** Faiz Ahmed Faiz, Saddar, I-8 (two hops from start)
- **Level 3:** PIMS (three hops — goal found!)

The FIFO queue ensures all Level 1 nodes are processed before any Level 2 node.

---

## TASK 2: Tree Search vs Graph Search

### What It Does
Demonstrates **3 configurations** of BFS on hospital navigation:

| Part | Structure | Visited Set | Behavior |
|------|-----------|-------------|----------|
| Part 1 | Tree (no cycles) | NOT used | Works fine |
| Part 2A | Graph (cycle) | NOT used | Repeated states, potential infinite loop |
| Part 2B | Graph (cycle) | USED | Terminates correctly |

### Key Answer Points

**Q: Why doesn't a tree need a visited set?**
> A tree has **no back-edges** — every node has exactly one path back to the root. No node can be reached twice through different paths. So no repeated states occur.

**Q: What is the cycle in Part 2A?**
> `Main Corridor → Waiting Area → Main Corridor → Waiting Area → ...`
> Without a visited set, each time Waiting Area is expanded, it re-adds Main Corridor, and vice versa.

**Q: What does `max_steps` do in Part 2A?**
> It's only a **safety limit for the demo** — it prevents the notebook from running forever. It's NOT part of the BFS concept. In real code without a visited set, this would loop infinitely.

**Q: How does the visited set fix the cycle?**
> When Waiting Area generates Main Corridor, the algorithm checks: `if neighbor not in visited`. Since Main Corridor was already visited, it's **skipped**. The cycle is broken.

**Q: What is the actual problem demonstrated?**
> Real-world environments are graphs (interconnected buildings, networks). Graph search algorithms **must** track explored states to handle cycles. Tree search assumptions don't hold for real environments.

**Q: Why is the tree traversal different from the path?**
> Traversal = ALL nodes visited in order (7 nodes). Path = only the solution route (4 nodes: Main Entrance → Emergency Lobby → Waiting Area → Radiology Department).

### Comparison Table (from lab)
| Feature | Tree | Graph |
|---------|------|-------|
| Multiple paths to same location | No | Yes |
| Back-edges | No | Possible |
| Cycles | No | Possible |
| Repeated states possible | No | Yes |
| BFS without visited set | Can work | Can fail/infinite loop |
| Visited set | Not required | Essential |

### Actual Outputs

**Part 1 (Tree):**
```
Traversal: Main Entrance → Reception → Emergency Lobby → Registration → Waiting Area → Main Corridor → Radiology Department
Path: Main Entrance → Emergency Lobby → Waiting Area → Radiology Department
```

**Part 2A (No visited set):**
```
Step 5: Waiting Area adds ['Radiology Department', 'Main Corridor'] → Queue: [..., 'Main Corridor', 'Waiting Area', 'Main Corridor']
Step 6: Main Corridor adds ['Waiting Area'] → Queue: [..., 'Main Corridor', 'Waiting Area']
```
→ Main Corridor and Waiting Area keep reappearing!

**Part 2B (With visited set):**
```
Step 6: Main Corridor → added: [] (empty — Waiting Area already visited)
Visited Set: {'Emergency Lobby', 'Registration', 'Reception', 'Main Corridor', 'Waiting Area', 'Main Entrance'}
Path: Main Entrance → Emergency Lobby → Waiting Area → Radiology Department
```

---

## TASK 3: DFS for Warehouse Robot Exploration

### What It Does
Robot searches from Receiving Area to Inspection Area using **Depth-First Search** — goes as deep as possible before backtracking.

### Key Answer Points

**Q: Why use a stack (LIFO)?**
> DFS explores the most recently discovered node first. `stack.pop()` removes from the END (last in, first out), so the deepest node is always explored next.

**Q: What is `reversed(graph[current])` for?**
> When we push neighbors in reversed order onto a stack, the LEFTMOST neighbor ends up on TOP of the stack and gets popped first. This makes DFS explore in the natural left-to-right order of the adjacency list.

**Q: What does "backtracking" mean?**
> When a node has no unvisited neighbors (dead end), `stack.pop()` takes us back to the previous node. Example: after Laptops (dead end), we backtrack to Main Aisle.

**Q: Why does DFS NOT guarantee shortest path?**
> DFS goes deep first. It might find the goal via a long path through one branch, even if a shorter path exists through another branch. In this case it found a 4-edge path (optimal), but that's not guaranteed.

**Q: Why is traversal order different from solution path?**
> Traversal = EVERY node popped from stack (includes dead ends, backtrack points). Solution path = only nodes from start to goal via parent pointers. DFS visits nodes in a different order than the final path.

**Q: How does DFS memory usage compare to BFS?**
> DFS stores only nodes on the current path + siblings on the stack. BFS stores ALL nodes at the current level. For wide graphs, BFS uses much more memory.

### Actual Output
```
Traversal: Receiving Area → Main Aisle → Electronics → Phones → Inspection Area
Path: Receiving Area → Main Aisle → Electronics → Phones → Inspection Area
Number of States Explored: 4
Stack trace: 
  Step 1: Pop Receiving Area, push Main Aisle
  Step 2: Pop Main Aisle, push Packaging/Grocery/Electronics (reversed → Electronics on top)
  Step 3: Pop Electronics, push Laptops/Phones (reversed → Phones on top)
  Step 4: Pop Phones, push Inspection Area
  Step 5: Pop Inspection Area → GOAL FOUND
```

**Why this order?** DFS goes: Receiving Area → Main Aisle → **Electronics** (first branch) → **Phones** → **Inspection Area**. It never explores Grocery or Packaging because it found the goal first!

**Key observation from lab:** "The exact DFS traversal can depend on the order in which neighbors are stored."

---

## TASK 4: UCS for Delivery Route Optimization

### What It Does
Finds the **minimum accumulated cost** route from Islamabad Delivery Hub to Blue Area Delivery Point.

### Key Answer Points

**Q: Why does UCS use a priority queue?**
> UCS must always expand the node with the **lowest cumulative path cost**. `heapq.heappop()` returns the smallest element — `(cost, node)` tuples are compared by cost first.

**Q: Why does UCS NOT find fewest edges?**
> BFS minimizes edges. UCS minimizes **sum of edge weights**. A 3-edge path costing 11 is worse than a 4-edge path costing 8. UCS picks the cheaper one regardless of edge count.

**Q: What is `best_cost` used for?**
> Stores the best known cost to reach each node. When we find a cheaper path to a node we've already seen, we update `best_cost` and re-add it to the queue. This handles the case where a cheaper route is found later.

**Q: Why check `if current in best_cost and current_cost > best_cost[current]`?**
> This is a **stale entry check**. A node might be in the priority queue multiple times (via different paths). If we pop it with a cost higher than what we already know, we skip it — we already have a better path.

**Q: What is the goal test timing?**
> Goal test when **popping from priority queue** — same reasoning as BFS. Since the priority queue always gives the lowest-cost node, popping the goal guarantees it's via the cheapest path.

**Q: What's the difference between UCS and Dijkstra's algorithm?**
> They're essentially the same for this use case. UCS stops when it pops the goal; Dijkstra continues until all nodes are processed.

### Actual Output
```
Step 1: POP Islamabad Delivery Hub (cost=0) → Add I-8 (cost=4), H-8 (cost=2)
Step 2: POP H-8 Markaz (cost=2) → Add G-8 (cost=5)
Step 3: POP I-8 Markaz (cost=4) → Add F-8 (cost=9), Blue Area (cost=12)
Step 4: POP G-8 Markaz (cost=5) → Add Blue Area (cost=11)
Step 5: POP F-8 Markaz (cost=9)
Step 6: POP Blue Area Delivery Point (cost=11) → GOAL FOUND

Solution: Islamabad Delivery Hub → H-8 Markaz → G-8 Markaz → Blue Area Delivery Point
Total Cost: 11
```

**Why this path?**
- Route 1 (via I-8): Hub → I-8 → Blue Area = 4 + 8 = **12**
- Route 2 (via H-8): Hub → H-8 → G-8 → Blue Area = 2 + 3 + 6 = **11** ✓ CHEAPEST
- Route 3 (via F-8): Hub → H-8 → G-8 → F-8 → Blue = 2 + 3 + 4 + 3 = **12**

UCS picks Route 2 because 11 < 12, even though it has 3 edges vs 2 edges for Route 1.

---

## TASK 5: Formal State-Space Modeling (Home Task)

### What It Does
Defines the formal problem representation for a hospital robot (Pharmacy → Emergency Department) **before** implementing any search algorithm.

### Key Answer Points

**Q: Why separate problem definition from search algorithm?**
> The lab teaches: "problem formulation comes before search algorithm implementation." The same graph/representation should work for BFS, DFS, and UCS — only the frontier selection logic changes. This is the core principle of AI problem-solving.

**Q: What is a successor function?**
> `get_successors(state)` returns all states reachable in one action from the current state. It encapsulates "what can I do from here?" — search algorithms call this to expand nodes.

**Q: What are the components of a search problem?**
> 1. **Initial State** — where we start
> 2. **Goal State** — what we're looking for
> 3. **States** — all possible configurations
> 4. **Actions** — possible transitions
> 5. **Successor Function** — returns neighbors of a state
> 6. **Cost Function** — cost of each transition
> 7. **Path** — sequence of states from start to goal

---

## TASK 6: Smart Building Navigation (Comparison)

### What It Does
Runs BFS, DFS, and UCS on the **same building** (Main Lobby → Conference Hall) and compares their behavior.

### Key Answer Points

**Q: Why do all three algorithms give different paths on the same graph?**
> Different frontier selection:
> - BFS uses FIFO queue → expands shallowest first → fewest edges
> - DFS uses LIFO stack → expands deepest first → may take winding path
> - UCS uses priority queue → expands lowest cost first → cheapest path

**Q: Is BFS optimal?**
> Yes for **minimum transitions** (edges). No for minimum cost in weighted graphs.

**Q: Is DFS optimal?**
> No — DFS is NOT optimal for either edges or cost. It's useful for deep exploration when memory is limited.

**Q: Is UCS optimal?**
> Yes for **minimum accumulated cost** when all edge costs are non-negative.

**Q: How do you determine which algorithm "worked"?**
> Each is "optimal" under its own objective:
> - BFS: optimal if minimizing transitions
> - DFS: never guaranteed optimal
> - UCS: optimal if minimizing total cost
> The purpose is not to find which "worked" but to understand WHY they differ.

---

## Common Questions the Examiner Might Ask

### General Uninformed Search

**Q: What is "uninformed" (blind) search?**
> It explores without any domain-specific knowledge or heuristics. It only uses: initial state, possible actions, goal test, and path cost. No additional information about which direction is "better."

**Q: What are the 5 key components of uninformed search?**
> 1. State representation
> 2. Frontier (list of nodes to expand)
> 3. Explored/visited set
> 4. Goal test
> 5. Node expansion (generating successors)

**Q: What is the frontier?**
> Nodes that are **generated but not yet expanded**. Different algorithms manage it differently:
> - BFS: Queue (FIFO)
> - DFS: Stack (LIFO)
> - UCS: Priority Queue (by cost)

**Q: Frontier vs Visited set?**
> - Frontier = discovered, waiting to be expanded
> - Visited = already expanded
> - A node moves from frontier → visited when it's popped and processed

**Q: Why can't BFS work on weighted graphs?**
> BFS assumes all edges have equal cost. On weighted graphs, a path with fewer edges might have higher total cost. For weighted graphs, use UCS.

**Q: Can DFS guarantee termination?**
> Only with a visited set on cyclic graphs. Without it, DFS can loop infinitely. On trees, it terminates naturally.

### Code-Level Questions

**Q: What does `parent = {start: None}` mean?**
> Start has no parent. The path reconstruction loop `while node is not None` stops when it reaches the start.

**Q: Why `path.reverse()`?**
> Parent pointers go goal → start (backwards). We reverse to get start → goal (forwards).

**Q: What does `neighbor not in queue` check do (in BFS)?**
> Prevents adding duplicate nodes to the queue. Without it, a node could be queued multiple times via different parents, wasting memory and time.

**Q: Why initialize `best_cost = {start: 0}` in UCS?**
> The start node has cost 0. This also prevents re-adding start to the queue if there's a cycle back to it.

**Q: What happens if the goal is unreachable?**
> BFS/DFS: queue/stack empties, loop ends, path is empty. UCS: priority queue empties. All return empty path gracefully.

---

## NetworkX Visualization Explained

**Q: How do you build a graph from a dictionary?**
```python
G = nx.DiGraph()
for node in graph:
    for neighbor in graph[node]:
        G.add_edge(node, neighbor)
```

**Q: How is the solution path highlighted?**
```python
path_edges = list(zip(path, path[1:]))  # Convert path to edge list
nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                       edge_color='red', width=4)
```

**Q: What does `nx.spring_layout(G, seed=42, k=2.5)` do?**
> Automatically positions nodes using a force-directed algorithm. `seed=42` makes positions deterministic (same every run). `k=2.5` spreads nodes apart.

**Q: How do you show edge weights for UCS?**
```python
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
```

---

## Quick Demo Script (30-second summary per task)

**Task 1:** "BFS on transport network. FIFO queue, level-by-level. Found 3-transition path: FAST → NUST → Faiz Ahmed Faiz → PIMS. Goal tested on pop, parent dictionary for path reconstruction."

**Task 2:** "Three runs: tree without visited works because no cycles. Graph without visited shows Main Corridor/Waiting Area repeating (cycle problem). Graph with visited set skips repeats and terminates normally."

**Task 3:** "DFS with LIFO stack. Went deep into Electronics → Phones → Inspection Area. Never explored Grocery or Packaging branches. Backtracking happens when a node has no unvisited neighbors."

**Task 4:** "UCS with heapq priority queue. Always expands lowest cumulative cost. Chose path costing 11 (3 edges) over path costing 12 (2 edges) — minimum cost, not minimum edges."

**Task 5:** "Formal problem definition: initial state, goal state, states, actions, successor function, cost function. Same representation works for BFS, DFS, UCS — only frontier changes."

**Task 6:** "Same building, three algorithms, three different behaviors. BFS=level-by-level (min edges), DFS=deep first (not optimal), UCS=min cost (optimal for weighted). Different frontier selection causes different results."
