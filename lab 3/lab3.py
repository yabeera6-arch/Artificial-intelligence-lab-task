from collections import deque; import heapq

graph = {"A": "BC", "B": "DE", "C": "F", "D": "", "E": "G", "F": "", "G": ""}

def bfs(graph, start, goal):
    queue = deque([[start]]); seen = {start}; order = []
    while queue:
        path = queue.popleft(); node = path[-1]; order.append(node)
        if node == goal: return path, order
        for nxt in graph[node]:
            if nxt not in seen: seen.add(nxt); queue.append(path + [nxt])
    return None, order

def dfs(graph, start, goal):
    stack = [[start]]; seen = set(); order = []
    while stack:
        path = stack.pop(); node = path[-1]
        if node in seen: continue
        seen.add(node); order.append(node)
        if node == goal: return path, order
        for nxt in reversed(graph[node]): stack.append(path + [nxt])
    return None, order

def dls(graph, start, goal, limit):
    def search(node, path, depth):
        if node == goal: return "FOUND", path
        if depth == limit: return "CUTOFF", None
        cutoff = False
        for nxt in graph[node]:
            if nxt in path: continue
            status, found = search(nxt, path + [nxt], depth + 1)
            if status == "FOUND": return status, found
            cutoff = cutoff or status == "CUTOFF"
        return ("CUTOFF" if cutoff else "FAILURE"), None
    return search(start, [start], 0)

def iddfs(graph, start, goal, max_depth):
    for limit in range(max_depth + 1):
        status, path = dls(graph, start, goal, limit)
        if status == "FOUND": return status, path, limit
    return "CUTOFF", None, max_depth

costs = {("A","B"):1, ("A","C"):6, ("B","D"):2, ("B","E"):1,
         ("C","F"):3, ("C","G"):6, ("E","G"):1}
wtop = {"A": "BC", "B": "DE", "C": "FG", "D": "", "E": "G", "F": "", "G": ""}

def ucs(start, goal):
    pq = [(0, [start])]; seen = set(); order = []
    while pq:
        cost, path = heapq.heappop(pq); node = path[-1]
        if node in seen: continue
        seen.add(node); order.append(node)
        if node == goal: return path, cost, order
        for nxt in wtop[node]:
            if nxt not in seen:
                heapq.heappush(pq, (cost + costs[(node, nxt)], path + [nxt]))
    return None, None, order

def path_cost(path):
    return sum(costs[pair] for pair in zip(path, path[1:]))

def check(name, got, want):
    print("PASS" if got == want else "FAIL", name, got)

path, order = bfs(graph, "A", "G")
check("bfs", (path, order), (["A","B","E","G"], list("ABCDEFG")))
path, order = dfs(graph, "A", "G")
check("dfs", (path, order), (["A","B","E","G"], ["A","B","D","E","G"]))
for limit in (1, 2, 3, 4):
    print("dls", limit, dls(graph, "A", "G", limit))
for max_d in (1, 2, 3, 4):
    print("iddfs", max_d, iddfs(graph, "A", "G", max_d))
path, total, order = ucs("A", "G")
check("ucs", (path, total, path_cost(path), order),
      (["A","B","E","G"], 3, 3, ["A","B","E","D","G"]))
bfs_path, _ = bfs(wtop, "A", "G")
check("bfs-weighted", (bfs_path, path_cost(bfs_path)), (["A","C","G"], 12))
check("start=goal", bfs(graph, "A", "A")[0], ["A"])
check("no-path", bfs(graph, "D", "G")[0], None)
cyclic = dict(graph); cyclic["F"] = "A"
check("cycle", (bfs(cyclic, "A", "F")[0], dls(cyclic, "A", "G", 4)[0]),
      (["A","C","F"], "FOUND"))
