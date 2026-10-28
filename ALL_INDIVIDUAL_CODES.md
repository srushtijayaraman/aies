# All AI Lab Codes — Combined Reference

Each program below is also available as a separate, independent source file. See `README.md` for execution instructions and dependencies.


---

## `01_State_Space/01_tower_of_hanoi.py`

```python
"""Tower of Hanoi: recursive state-space solution. Standard library only."""

def hanoi(n, source="A", auxiliary="B", target="C"):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n - 1, source, target, auxiliary)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, auxiliary, source, target)

if __name__ == "__main__":
    raw = input("Number of disks [3]: ").strip()
    n = int(raw) if raw else 3
    if not 1 <= n <= 20:
        raise SystemExit("Choose between 1 and 20 disks to avoid enormous output.")
    hanoi(n)
    print(f"Minimum moves: {2**n - 1}")
```


---

## `01_State_Space/02_missionaries_cannibals_bfs.py`

```python
"""Shortest solution to the 3 missionaries and 3 cannibals puzzle using BFS."""
from collections import deque

TOTAL = 3
BOAT_MOVES = ((1, 0), (2, 0), (0, 1), (0, 2), (1, 1))
# State: (missionaries_left, cannibals_left, boat_on_left [1=yes, 0=no])
START, GOAL = (3, 3, 1), (0, 0, 0)

def safe(m, c):
    if not (0 <= m <= TOTAL and 0 <= c <= TOTAL):
        return False
    right_m, right_c = TOTAL - m, TOTAL - c
    return (m == 0 or m >= c) and (right_m == 0 or right_m >= right_c)

def successors(state):
    m, c, boat_left = state
    for dm, dc in BOAT_MOVES:
        if boat_left:
            nxt = (m - dm, c - dc, 0)
            direction = "left -> right"
        else:
            nxt = (m + dm, c + dc, 1)
            direction = "right -> left"
        if safe(nxt[0], nxt[1]):
            yield nxt, f"Move {dm} missionary/ies and {dc} cannibal(s), {direction}"

def solve():
    queue = deque([START])
    parent = {START: None}
    action = {}
    while queue:
        state = queue.popleft()
        if state == GOAL:
            break
        for nxt, move in successors(state):
            if nxt not in parent:
                parent[nxt] = state
                action[nxt] = move
                queue.append(nxt)
    if GOAL not in parent:
        print("No solution found.")
        return
    path = []
    s = GOAL
    while s is not None:
        path.append(s)
        s = parent[s]
    path.reverse()
    print("State = (missionaries left, cannibals left, boat side L=left/R=right)")
    for i, s in enumerate(path):
        print(f"{i}: {s[0]}M, {s[1]}C, boat={'L' if s[2] else 'R'}")
        if i:
            print("   " + action[s])
    print(f"Crossings: {len(path)-1}")

if __name__ == "__main__":
    solve()
```


---

## `01_State_Space/03_water_jug_bfs.py`

```python
"""Water jug problem solved with BFS. Default: 4L and 3L jugs, target 2L."""
from collections import deque

CAP_A, CAP_B, TARGET = 4, 3, 2
START = (0, 0)

def successors(state):
    a, b = state
    # Fill, empty, and pour. Each action costs one move.
    candidates = [
        ((CAP_A, b), "Fill 4L jug"),
        ((a, CAP_B), "Fill 3L jug"),
        ((0, b), "Empty 4L jug"),
        ((a, 0), "Empty 3L jug"),
    ]
    pour = min(a, CAP_B - b)
    candidates.append(((a - pour, b + pour), "Pour 4L -> 3L"))
    pour = min(b, CAP_A - a)
    candidates.append(((a + pour, b - pour), "Pour 3L -> 4L"))
    seen = set()
    for nxt, label in candidates:
        if nxt != state and nxt not in seen:
            seen.add(nxt)
            yield nxt, label

def solve():
    q = deque([START])
    parent = {START: None}
    action = {}
    goal = None
    while q:
        s = q.popleft()
        if TARGET in s:
            goal = s
            break
        for nxt, move in successors(s):
            if nxt not in parent:
                parent[nxt] = s
                action[nxt] = move
                q.append(nxt)
    if goal is None:
        print("Target amount is unreachable with these jug capacities.")
        return
    path, s = [], goal
    while s is not None:
        path.append(s)
        s = parent[s]
    path.reverse()
    print("State = (water in 4L jug, water in 3L jug)")
    for i, state in enumerate(path):
        print(f"{i}: {state}")
        if i:
            print("   " + action[state])
    print(f"Moves: {len(path)-1}")

if __name__ == "__main__":
    solve()
```


---

## `01_State_Space/04_graph_bfs_dfs.py`

```python
"""Small standalone BFS and DFS example for state-space graph search."""
from collections import deque

GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": ["G"], "E": ["G"], "F": ["G"], "G": []
}

def bfs(start, goal):
    queue = deque([start])
    parent = {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for nxt in GRAPH[node]:
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    return build_path(parent, goal)

def dfs(start, goal):
    stack = [start]
    parent = {start: None}
    while stack:
        node = stack.pop()
        if node == goal:
            break
        for nxt in reversed(GRAPH[node]):
            if nxt not in parent:
                parent[nxt] = node
                stack.append(nxt)
    return build_path(parent, goal)

def build_path(parent, goal):
    if goal not in parent:
        return None
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]

if __name__ == "__main__":
    print("BFS shortest path A -> G:", bfs("A", "G"))
    print("DFS path A -> G:         ", dfs("A", "G"))
```


---

## `02_Astar/05_eight_puzzle_astar.py`

```python
"""Optimal A* solution for the 8-puzzle using Manhattan distance."""
import heapq
from itertools import count

DEFAULT_START = (1, 2, 3,
                 4, 0, 6,
                 7, 5, 8)
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)
GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL)}

def solvable(state):
    nums = [x for x in state if x != 0]
    inversions = sum(nums[i] > nums[j]
                     for i in range(len(nums))
                     for j in range(i + 1, len(nums)))
    return inversions % 2 == 0  # 3x3 board has odd width

def heuristic(state):
    total = 0
    for i, tile in enumerate(state):
        if tile:
            r, c = divmod(i, 3)
            gr, gc = GOAL_POS[tile]
            total += abs(r - gr) + abs(c - gc)
    return total

def neighbors(state):
    blank = state.index(0)
    r, c = divmod(blank, 3)
    for nr, nc in ((r-1,c), (r+1,c), (r,c-1), (r,c+1)):
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            board = list(state)
            board[blank], board[j] = board[j], board[blank]
            yield tuple(board)

def astar(start):
    if not solvable(start):
        return None
    tie = count()
    open_heap = [(heuristic(start), heuristic(start), next(tie), 0, start)]
    best_g = {start: 0}
    parent = {start: None}
    while open_heap:
        _, _, _, g, state = heapq.heappop(open_heap)
        if g != best_g.get(state):  # ignore stale heap entries
            continue
        if state == GOAL:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]
        for nxt in neighbors(state):
            ng = g + 1
            if ng < best_g.get(nxt, float("inf")):
                best_g[nxt] = ng
                parent[nxt] = state
                h = heuristic(nxt)
                heapq.heappush(open_heap, (ng+h, h, next(tie), ng, nxt))
    return None

def print_board(state):
    for i in range(0, 9, 3):
        print(" ".join("_" if x == 0 else str(x) for x in state[i:i+3]))
    print()

if __name__ == "__main__":
    print("Enter 9 numbers separated by spaces (0 = blank), or press Enter for demo.")
    raw = input("Initial board: ").strip()
    start = tuple(map(int, raw.split())) if raw else DEFAULT_START
    if len(start) != 9 or set(start) != set(range(9)):
        raise SystemExit("Board must contain each number 0 through 8 exactly once.")
    if not solvable(start):
        raise SystemExit("This board cannot reach the specified goal state.")
    path = astar(start)
    for i, state in enumerate(path):
        print(f"Step {i}:")
        print_board(state)
    print("Optimal number of moves:", len(path) - 1)
```


---

## `03_Local_Search/06_tsp_hill_climbing_2opt.py`

```python
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
```


---

## `03_Local_Search/07_tsp_exact_held_karp.py`

```python
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
```


---

## `03_Local_Search/08_n_queens_min_conflicts.py`

```python
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
```


---

## `03_Local_Search/09_tsp_genetic_algorithm.py`

```python
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
```


---

## `04_CSP/09_send_more_money.py`

```python
"""Column-wise backtracking solver for SEND + MORE = MONEY."""

def solve_cryptarithm(addends, result):
    words = addends + [result]
    leading = {word[0] for word in words if len(word) > 1}
    letters = set("".join(words))
    if len(letters) > 10:
        raise ValueError("More than 10 distinct letters cannot map to distinct decimal digits.")
    mapping, used = {}, set()
    max_cols = len(result)

    def assign_column(col, carry):
        if col == max_cols:
            return mapping.copy() if carry == 0 else None
        chars = [w[-1-col] for w in addends if col < len(w)]

        def sum_chars(i, subtotal):
            if i == len(chars):
                total = subtotal + carry
                digit, next_carry = total % 10, total // 10
                rch = result[-1-col]
                if rch in mapping:
                    if mapping[rch] != digit:
                        return None
                    return assign_column(col + 1, next_carry)
                if digit in used or (digit == 0 and rch in leading):
                    return None
                mapping[rch], used_digit = digit, digit
                used.add(used_digit)
                answer = assign_column(col + 1, next_carry)
                if answer is not None:
                    return answer
                used.remove(used_digit)
                del mapping[rch]
                return None
            ch = chars[i]
            if ch in mapping:
                return sum_chars(i + 1, subtotal + mapping[ch])
            for digit in range(10):
                if digit in used or (digit == 0 and ch in leading):
                    continue
                mapping[ch] = digit
                used.add(digit)
                answer = sum_chars(i + 1, subtotal + digit)
                if answer is not None:
                    return answer
                used.remove(digit)
                del mapping[ch]
            return None
        return sum_chars(0, 0)

    return assign_column(0, 0)

def value(word, mapping):
    return int("".join(str(mapping[ch]) for ch in word))

if __name__ == "__main__":
    solution = solve_cryptarithm(["SEND", "MORE"], "MONEY")
    if solution:
        for letter in sorted(solution):
            print(f"{letter} = {solution[letter]}")
        a, b, total = (value(w, solution) for w in ["SEND", "MORE", "MONEY"])
        print(f"{a} + {b} = {total}")
    else:
        print("No solution found.")
```


---

## `04_CSP/10_cross_roads_danger.py`

```python
"""Column-wise backtracking solver for CROSS + ROADS = DANGER."""
# Self-contained cryptarithmetic CSP solver; assigns distinct digits to letters.

def solve_cryptarithm(addends, result):
    words = addends + [result]
    leading = {word[0] for word in words if len(word) > 1}
    letters = set("".join(words))
    if len(letters) > 10:
        raise ValueError("More than 10 distinct letters cannot map to distinct digits.")
    mapping, used = {}, set()

    def column(col, carry):
        if col == len(result):
            return mapping.copy() if carry == 0 else None
        chars = [w[-1-col] for w in addends if col < len(w)]
        def add_letters(i, subtotal):
            if i == len(chars):
                total = subtotal + carry
                digit, next_carry = total % 10, total // 10
                ch = result[-1-col]
                if ch in mapping:
                    return column(col+1, next_carry) if mapping[ch] == digit else None
                if digit in used or (digit == 0 and ch in leading):
                    return None
                mapping[ch] = digit; used.add(digit)
                answer = column(col+1, next_carry)
                if answer is not None:
                    return answer
                used.remove(digit); del mapping[ch]
                return None
            ch = chars[i]
            if ch in mapping:
                return add_letters(i+1, subtotal + mapping[ch])
            for d in range(10):
                if d in used or (d == 0 and ch in leading):
                    continue
                mapping[ch] = d; used.add(d)
                answer = add_letters(i+1, subtotal+d)
                if answer is not None:
                    return answer
                used.remove(d); del mapping[ch]
            return None
        return add_letters(0, 0)
    return column(0, 0)

def value(word, mapping):
    return int("".join(str(mapping[ch]) for ch in word))

if __name__ == "__main__":
    solution = solve_cryptarithm(["CROSS", "ROADS"], "DANGER")
    if solution:
        for letter in sorted(solution):
            print(f"{letter} = {solution[letter]}")
        a, b, total = (value(w, solution) for w in ["CROSS", "ROADS", "DANGER"])
        print(f"{a} + {b} = {total}")
    else:
        print("No solution found.")
```


---

## `05_Minimax/11_tic_tac_toe_minimax_alphabeta.py`

```python
"""Playable Tic-Tac-Toe: human X, optimal computer O, Minimax + alpha-beta."""
HUMAN, AI, EMPTY = "X", "O", " "
WIN_LINES = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
MOVE_ORDER = (4, 0, 2, 6, 8, 1, 3, 5, 7)  # good moves first for alpha-beta pruning

def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None

def minimax(board, maximizing, depth, alpha, beta):
    result = winner(board)
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if EMPTY not in board:
        return 0
    if maximizing:  # AI O maximises the score
        best = -float("inf")
        for i in MOVE_ORDER:
            if board[i] == EMPTY:
                board[i] = AI
                best = max(best, minimax(board, False, depth+1, alpha, beta))
                board[i] = EMPTY
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best
    best = float("inf")
    for i in MOVE_ORDER:
        if board[i] == EMPTY:
            board[i] = HUMAN
            best = min(best, minimax(board, True, depth+1, alpha, beta))
            board[i] = EMPTY
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best

def best_ai_move(board):
    best_score, best_move = -float("inf"), None
    for i in MOVE_ORDER:
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, False, 1, -float("inf"), float("inf"))
            board[i] = EMPTY
            if score > best_score:
                best_score, best_move = score, i
    return best_move

def show(board):
    cells = [str(i+1) if x == EMPTY else x for i, x in enumerate(board)]
    print(f" {cells[0]} | {cells[1]} | {cells[2]}\n---+---+---\n {cells[3]} | {cells[4]} | {cells[5]}\n---+---+---\n {cells[6]} | {cells[7]} | {cells[8]}\n")

if __name__ == "__main__":
    board = [EMPTY] * 9
    print("You are X; the computer is O. Choose a cell from 1 to 9.")
    show(board)
    while True:
        try:
            move = int(input("Your move (1-9): ")) - 1
            if not 0 <= move < 9 or board[move] != EMPTY:
                print("That cell is not available. Try again.")
                continue
        except EOFError:
            print("\nInput ended; game stopped.")
            break
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue
        board[move] = HUMAN
        show(board)
        if winner(board) == HUMAN:
            print("You win!"); break
        if EMPTY not in board:
            print("Draw!"); break
        ai_move = best_ai_move(board)
        board[ai_move] = AI
        print(f"Computer chooses cell {ai_move+1}.")
        show(board)
        if winner(board) == AI:
            print("Computer wins."); break
        if EMPTY not in board:
            print("Draw!"); break
```


---

## `06_Expert_System/12_expert_system_prolog.pl`

```prolog
% Mini expert system in SWI-Prolog.
% Load with: ?- [expert_system_prolog].
% Query with: ?- recommendation(X).

% Example facts (edit these to test different cases).
symptom(no_internet).
symptom(router_light_red).
% symptom(router_light_green).
% symptom(single_device_only).

recommendation(check_router_power_and_cables) :-
    symptom(no_internet),
    symptom(router_light_red).

recommendation(check_wifi_or_network_settings) :-
    symptom(no_internet),
    symptom(router_light_green).

recommendation(check_device_settings) :-
    symptom(no_internet),
    symptom(single_device_only).

recommendation(contact_internet_provider) :-
    symptom(no_internet),
    symptom(router_light_green),
    symptom(all_devices_affected).

% Catch-all advice if no specific rule is supported.
recommendation(run_general_network_checklist) :-
    \+ recommendation(check_router_power_and_cables),
    \+ recommendation(check_wifi_or_network_settings),
    \+ recommendation(check_device_settings),
    \+ recommendation(contact_internet_provider).
```


---

## `06_Expert_System/13_expert_system_python.py`

```python
"""Interactive rule-based expert system (Python equivalent of the Prolog lab)."""

def yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer y or n.")

if __name__ == "__main__":
    print("Mini Network Troubleshooting Expert System")
    no_internet = yes_no("Is there no internet connection?")
    if not no_internet:
        print("Advice: Your connection appears to be working. Check the specific app if needed.")
    else:
        red = yes_no("Is the router light red or showing an error?")
        one_device = yes_no("Is the issue limited to only one device?")
        if red:
            print("Advice: Check router power, cables, and the ISP connection.")
        elif one_device:
            print("Advice: Check that device's Wi-Fi settings, airplane mode, and network adapter.")
        else:
            print("Advice: Restart the router; if all devices remain offline, contact your ISP.")
```


---

## `07_Chatbot/14_chatbot_rule_based.py`

```python
"""Standalone rule-based chatbot; no external libraries required."""
import re

def reply(message):
    text = message.lower().strip()
    words = set(re.findall(r"[a-z']+", text))
    if not text:
        return "Please type a message."
    if words & {"bye", "goodbye", "quit", "exit"}:
        return "Goodbye!"
    if words & {"hi", "hello", "hey", "morning"}:
        return "Hello! How can I help you?"
    if "thank" in words or "thanks" in words:
        return "You're welcome!"
    if words & {"help", "features", "do"}:
        return "I can answer basic greetings, help requests, and course questions."
    if "assignment" in words or "lab" in words:
        return "Tell me which AI lab assignment you are working on."
    if "time" in words or "hours" in words:
        return "Please check the official timetable or opening-hours notice."
    return "I did not understand that. Try asking in a different way."

if __name__ == "__main__":
    print("Bot: Hi! Type 'exit' to quit.")
    while True:
        message = input("You: ")
        answer = reply(message)
        print("Bot:", answer)
        if set(re.findall(r"[a-z']+", message.lower())) & {"bye", "goodbye", "quit", "exit"}:
            break
```


---

## `07_Chatbot/15_chatbot_tfidf_sklearn.py`

```python
"""Optional ML chatbot using TF-IDF + logistic regression.
Install: python -m pip install scikit-learn
This is a small educational intent classifier, not a generative AI assistant.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

examples = [
    "hello", "hi there", "good morning", "hey", "goodbye", "bye", "see you",
    "thank you", "thanks a lot", "help me", "what can you do", "show features",
    "when are you open", "what are your hours", "show the timetable", "class schedule"
]
labels = [
    "greeting", "greeting", "greeting", "greeting", "goodbye", "goodbye", "goodbye",
    "thanks", "thanks", "help", "help", "help", "hours", "hours", "schedule", "schedule"
]
responses = {
    "greeting": "Hello! How can I help?",
    "goodbye": "Goodbye!",
    "thanks": "You're welcome!",
    "help": "I can answer basic questions. Add more training examples to expand me.",
    "hours": "Please check the official opening-hours notice.",
    "schedule": "Please check the official timetable.",
    "unknown": "I am not sure I understood. Could you rephrase?"
}
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000))
model.fit(examples, labels)

if __name__ == "__main__":
    print("Bot: Hello! Type exit to stop.")
    while True:
        text = input("You: ").strip()
        if text.lower() in {"exit", "quit", "bye"}:
            print("Bot:", responses["goodbye"])
            break
        if not text:
            print("Bot: Please type a message.")
            continue
        probabilities = model.predict_proba([text])[0]
        idx = probabilities.argmax()
        intent = model.classes_[idx] if probabilities[idx] >= 0.40 else "unknown"
        print("Bot:", responses[intent])
```


---

## `08_Face_Vision/16_face_detection_haar.py`

```python
"""Face detection using OpenCV's pre-trained Haar cascade.
Install: python -m pip install opencv-python
Put face.jpg next to this script, or pass an image path as an argument.
"""
import sys
from pathlib import Path
import cv2

image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("face.jpg")
image = cv2.imread(str(image_path))
if image is None:
    raise SystemExit(f"Cannot read image: {image_path}. Check the path.")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
model_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(model_path)
if cascade.empty():
    raise SystemExit("Could not load OpenCV Haar cascade.")
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
print("Faces detected:", len(faces))
out_path = image_path.with_name(image_path.stem + "_haar_detected.jpg")
cv2.imwrite(str(out_path), image)
print("Saved result:", out_path)
cv2.imshow("Haar Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```


---

## `08_Face_Vision/17_face_detection_yunet_dnn.py`

```python
"""Neural-network face detection using OpenCV YuNet (ONNX model required).
Install: python -m pip install opencv-python
Download face_detection_yunet_2023mar.onnx from the OpenCV Zoo model folder
and put it beside this script. Input image defaults to face.jpg.
"""
import sys
from pathlib import Path
import cv2

image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("face.jpg")
model_path = Path("face_detection_yunet_2023mar.onnx")
image = cv2.imread(str(image_path))
if image is None:
    raise SystemExit(f"Cannot read image: {image_path}")
if not model_path.exists():
    raise SystemExit("Missing face_detection_yunet_2023mar.onnx. See README for official download link.")
h, w = image.shape[:2]
detector = cv2.FaceDetectorYN.create(str(model_path), "", (w, h), 0.9, 0.3, 5000)
_, faces = detector.detect(image)
count = 0 if faces is None else len(faces)
if faces is not None:
    for face in faces:
        x, y, fw, fh = face[:4].astype(int)
        cv2.rectangle(image, (x, y), (x+fw, y+fh), (0, 255, 0), 2)
print("Faces detected:", count)
out_path = image_path.with_name(image_path.stem + "_yunet_detected.jpg")
cv2.imwrite(str(out_path), image)
print("Saved result:", out_path)
cv2.imshow("YuNet DNN Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```


---

## `08_Face_Vision/18_face_match_yunet_sface.py`

```python
"""Compare whether two images likely contain the same face using YuNet + SFace.
Requires the two ONNX model files from OpenCV Zoo and opencv-python.
This is biometric matching; use only images you have permission to process.
"""
from pathlib import Path
import cv2

DETECTOR_MODEL = Path("face_detection_yunet_2023mar.onnx")
RECOGNIZER_MODEL = Path("face_recognition_sface_2021dec.onnx")
IMAGE_1, IMAGE_2 = Path("face1.jpg"), Path("face2.jpg")
THRESHOLD_COSINE = 0.363  # OpenCV Zoo SFace example's reference threshold

def detect_largest_face(image, detector):
    h, w = image.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(image)
    if faces is None or len(faces) == 0:
        raise ValueError("No face detected in an input image.")
    return max(faces, key=lambda f: f[2] * f[3])

for file in (DETECTOR_MODEL, RECOGNIZER_MODEL, IMAGE_1, IMAGE_2):
    if not file.exists():
        raise SystemExit(f"Missing {file}. See README for model links and image setup.")
img1, img2 = cv2.imread(str(IMAGE_1)), cv2.imread(str(IMAGE_2))
if img1 is None or img2 is None:
    raise SystemExit("Could not read face1.jpg or face2.jpg.")
detector = cv2.FaceDetectorYN.create(str(DETECTOR_MODEL), "", (320, 320), 0.9, 0.3, 5000)
recognizer = cv2.FaceRecognizerSF.create(str(RECOGNIZER_MODEL), "")
face1 = detect_largest_face(img1, detector)
face2 = detect_largest_face(img2, detector)
aligned1 = recognizer.alignCrop(img1, face1)
aligned2 = recognizer.alignCrop(img2, face2)
feature1 = recognizer.feature(aligned1)
feature2 = recognizer.feature(aligned2)
score = recognizer.match(feature1, feature2, 0)  # 0 = cosine similarity in OpenCV SFace
print(f"Cosine similarity: {score:.4f}")
print("Likely same person" if score >= THRESHOLD_COSINE else "Likely different people")
print("This is an automated similarity estimate, not proof of identity.")
```
