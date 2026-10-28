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
