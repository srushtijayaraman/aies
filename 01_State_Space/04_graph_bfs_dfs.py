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
