# Task 1: Smart Parking Space Analysis (Beginner Version)
# AI-2002 Lab

# ---------- Data ----------
parking_data = [
    {"id": "A01", "zone": "A", "status": "occupied", "rate": 100},
    {"id": "A02", "zone": "A", "status": "available", "rate": 100},
    {"id": "B01", "zone": "B", "status": "occupied", "rate": 80},
    {"id": "B02", "zone": "B", "status": "available", "rate": 80},
    {"id": "C01", "zone": "C", "status": "available", "rate": 120},
    {"id": "C02", "zone": "C", "status": "occupied", "rate": 120}
]

print("=== Parking Data Loaded ===\n")

# ---------- 1. Display all available spaces ----------
print("--- Available Parking Spaces ---")
available_spaces = []   # we'll store the available ones here

for space in parking_data:
    if space["status"] == "available":
        print("ID:", space["id"], "Zone:", space["zone"], "Rate:", space["rate"], "PKR/hour")
        available_spaces.append(space)

print("\n")   # blank line

# ---------- 2. Store unique zones in a set ----------
zones = set()   # empty set
for space in parking_data:
    zones.add(space["zone"])
print("Unique zones:", zones)

print("\n")

# ---------- 3. Count available and occupied ----------
available_count = 0
occupied_count = 0

for space in parking_data:
    if space["status"] == "available":
        available_count = available_count + 1
    else:
        occupied_count = occupied_count + 1

print("Available spaces:", available_count)
print("Occupied spaces:", occupied_count)

print("\n")

# ---------- 4. Define a function to calculate cost ----------
def calculate_cost(rate, hours):
    cost = rate * hours
    return cost

# ---------- 5. Rank available spaces by rate (cheapest first) using lambda ----------
# We'll use sorted() with a lambda that says "take the 'rate' from each space"
ranked_spaces = sorted(available_spaces, key=lambda x: x["rate"])

print("--- Available spaces ranked by rate (cheapest first) ---")
for space in ranked_spaces:
    print("ID:", space["id"], "Zone:", space["zone"], "Rate:", space["rate"], "PKR/hour")

print("\n")

# ---------- 6. & 7. Ask user for hours, show cost for each available space, and find cheapest ----------
hours_input = input("Enter number of parking hours: ")
hours = float(hours_input)   # convert to number

print("\n--- Estimated costs for available spaces ---")
cheapest_space = None        # we'll keep track of the cheapest
cheapest_cost = None

for space in available_spaces:
    cost = calculate_cost(space["rate"], hours)
    print("Space", space["id"], "(Zone", space["zone"], "): PKR", cost, "for", hours, "hour(s)")

    # update cheapest if this is the first or if cost is lower
    if cheapest_space is None or cost < cheapest_cost:
        cheapest_space = space
        cheapest_cost = cost

# Display the cheapest option
print("\n--- Cheapest available option ---")
print("Space ID:", cheapest_space["id"])
print("Zone:", cheapest_space["zone"])
print("Rate:", cheapest_space["rate"], "PKR/hour")
print("Total cost for", hours, "hour(s): PKR", cheapest_cost)