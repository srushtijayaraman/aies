"""Exact TSP solver using Held-Karp dynamic programming (O(n^2 * 2^n)).
Use for small/medium n when a provably optimal tour is needed.
"""
CITIES = ["A", "B", "C", "D", "E", "F"]
DIST = [
    [0, 10, 15, 20, 18, 12],
    [10, 0, 35, 25, 17, 28],
    [15, 35, 0, 30, 22, 16],
    [20, 25, 30, 0, 14, 24],
    [18, 17, 22, 14, 0, 13],
    [12, 28, 16, 24, 13, 0],
]

def held_karp(dist):
    n = len(dist)
    if n == 1:
        return [0, 0], 0
    # dp[(mask, j)] = cheapest path from 0 through mask, ending at j.
    dp, parent = {}, {}
    for j in range(1, n):
        mask = 1 << (j - 1)
        dp[(mask, j)] = dist[0][j]
        parent[(mask, j)] = 0
    for mask in range(1, 1 << (n - 1)):
        for j in range(1, n):
            if not mask & (1 << (j - 1)):
                continue
            prev_mask = mask ^ (1 << (j - 1))
            if prev_mask == 0:
                continue  # singleton states were initialized above
            best = float("inf")
            best_prev = None
            for k in range(1, n):
                if prev_mask & (1 << (k - 1)) and (prev_mask, k) in dp:
                    cost = dp[(prev_mask, k)] + dist[k][j]
                    if cost < best:
                        best, best_prev = cost, k
            dp[(mask, j)] = best
            parent[(mask, j)] = best_prev
    full = (1 << (n - 1)) - 1
    end = min(range(1, n), key=lambda j: dp[(full, j)] + dist[j][0])
    best_cost = dp[(full, end)] + dist[end][0]
    reverse_path = [end]
    mask, j = full, end
    while True:
        prev = parent[(mask, j)]
        mask ^= 1 << (j - 1)
        if prev == 0:
            break
        reverse_path.append(prev)
        j = prev
    route = [0] + reverse_path[::-1] + [0]
    return route, best_cost

if __name__ == "__main__":
    route, cost = held_karp(DIST)
    print("Optimal tour:", " -> ".join(CITIES[i] for i in route))
    print("Optimal distance:", cost)
