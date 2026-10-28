"""N-Queens using min-conflicts local search with random restarts."""
import random

def solve_n_queens(n=8, restarts=50, steps_per_restart=10000, seed=7):
    if n < 1:
        raise ValueError("n must be positive")
    if n in (2, 3):
        return None
    rng = random.Random(seed)
    for _ in range(restarts):
        # One queen per column; queens[c] gives row in column c.
        queens = [rng.randrange(n) for _ in range(n)]
        row_count = [0] * n
        down_count = [0] * (2*n - 1)  # row - col + n - 1
        up_count = [0] * (2*n - 1)    # row + col
        def alter(c, r, delta):
            row_count[r] += delta
            down_count[r-c+n-1] += delta
            up_count[r+c] += delta
        for c, r in enumerate(queens):
            alter(c, r, 1)
        for _step in range(steps_per_restart):
            conflicted = [c for c, r in enumerate(queens)
                          if row_count[r] + down_count[r-c+n-1]
                             + up_count[r+c] > 3]
            if not conflicted:
                return queens
            c = rng.choice(conflicted)
            old = queens[c]
            alter(c, old, -1)
            scores = [row_count[r] + down_count[r-c+n-1] + up_count[r+c]
                      for r in range(n)]
            minimum = min(scores)
            choices = [r for r, score in enumerate(scores) if score == minimum]
            new = rng.choice(choices)
            queens[c] = new
            alter(c, new, 1)
    return None

if __name__ == "__main__":
    raw = input("Number of queens [8]: ").strip()
    n = int(raw) if raw else 8
    solution = solve_n_queens(n)
    if solution is None:
        print(f"No solution found for n={n} with the configured search; n=2 and n=3 are impossible.")
    else:
        print("Row for each column (0-based):", solution)
        for r in range(n):
            print(" ".join("Q" if solution[c] == r else "." for c in range(n)))
