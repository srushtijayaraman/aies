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
