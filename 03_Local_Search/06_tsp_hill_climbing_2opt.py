"""TSP with steepest-descent hill climbing, 2-opt neighbors, and random restarts.
Returns the best tour found (not a proof of global optimality). Standard library only.
"""
import random

CITIES = ["A", "B", "C", "D", "E", "F"]
DIST = [
    [0, 10, 15, 20, 18, 12],
    [10, 0, 35, 25, 17, 28],
    [15, 35, 0, 30, 22, 16],
    [20, 25, 30, 0, 14, 24],
    [18, 17, 22, 14, 0, 13],
    [12, 28, 16, 24, 13, 0],
]

def tour_cost(route):
    return sum(DIST[route[i]][route[(i + 1) % len(route)]]
               for i in range(len(route)))

def hill_climb(initial):
    current = initial[:]
    while True:
        best, best_cost = current, tour_cost(current)
        n = len(current)
        # Keep city 0 first to avoid equivalent rotations of the same cycle.
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                candidate = current[:]
                candidate[i:j+1] = reversed(candidate[i:j+1])
                cost = tour_cost(candidate)
                if cost < best_cost:
                    best, best_cost = candidate, cost
        if best == current:
            return current
        current = best

def solve(restarts=100, seed=42):
    random.seed(seed)
    best_route, best_cost = None, float("inf")
    for _ in range(restarts):
        route = [0] + random.sample(range(1, len(CITIES)), len(CITIES) - 1)
        route = hill_climb(route)
        cost = tour_cost(route)
        if cost < best_cost:
            best_route, best_cost = route, cost
    return best_route, best_cost

if __name__ == "__main__":
    route, cost = solve()
    names = [CITIES[i] for i in route + [route[0]]]
    print("Best tour found:", " -> ".join(names))
    print("Total distance:", cost)
    print("Edit CITIES and DIST to use your own distance matrix.")
