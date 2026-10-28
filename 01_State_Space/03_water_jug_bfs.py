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
