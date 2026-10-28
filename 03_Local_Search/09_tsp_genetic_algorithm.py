"""Optional Genetic Algorithm for the TSP (permutation encoding + order crossover).
This is a heuristic optimizer, not a proof of global optimality.
Standard library only.
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

def cost(route):
    return sum(DIST[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))

def order_crossover(a, b, rng):
    """Order crossover (OX) preserves a valid city permutation."""
    n = len(a)
    left, right = sorted(rng.sample(range(n), 2))
    child = [-1] * n
    child[left:right+1] = a[left:right+1]
    fill = [x for x in b if x not in child]
    k = 0
    for i in list(range(right+1, n)) + list(range(0, left)):
        child[i] = fill[k]
        k += 1
    return child

def genetic_tsp(population_size=100, generations=500, seed=42):
    rng = random.Random(seed)
    n = len(CITIES)
    if n < 3:
        route = list(range(n))
        return route, cost(route)
    # Fix city 0 as the start to remove equivalent rotated tours.
    population = [[0] + rng.sample(range(1, n), n-1) for _ in range(population_size)]
    best = min(population, key=cost)[:]
    for _ in range(generations):
        population.sort(key=cost)
        if cost(population[0]) < cost(best):
            best = population[0][:]
        next_pop = [population[0][:], population[1][:]]  # elitism: keep two best
        def tournament(k=4):
            return min(rng.sample(population, min(k, len(population))), key=cost)
        while len(next_pop) < population_size:
            p1, p2 = tournament(), tournament()
            child = order_crossover(p1[1:], p2[1:], rng)
            child = [0] + child
            # Mutate in place while keeping city 0 fixed.
            if rng.random() < 0.15:
                i, j = rng.sample(range(1, n), 2)
                child[i], child[j] = child[j], child[i]
            next_pop.append(child)
        population = next_pop
    candidate = min(population, key=cost)
    if cost(candidate) < cost(best):
        best = candidate[:]
    return best, cost(best)

if __name__ == "__main__":
    route, distance = genetic_tsp()
    print("Best tour found:", " -> ".join(CITIES[i] for i in route + [route[0]]))
    print("Distance:", distance)
    print("For a guaranteed optimum on a small input, use 07_tsp_exact_held_karp.py.")
