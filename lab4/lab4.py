import heapq

graph = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
heuristic = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

def astar(graph, h, start, goal):
    queue = [(h[start], 0, start, [start])]
    best = {start: 0}
    order = []
    while queue:
        f, g, node, path = heapq.heappop(queue)
        if g != best[node]:
            continue
        order.append((node, g, h[node], f))
        if node == goal:
            return g, path, order
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(queue, (ng + h[nxt], ng, nxt, path + [nxt]))
    return None, None, order

def show(title, h):
    g, path, order = astar(graph, h, "S", "G")
    check = sum(dict(graph[a])[b] for a, b in zip(path, path[1:]))
    expanded = [n for n, _, _, _ in order if n != "G"]
    back = {}
    for n, edges in graph.items():
        for m, w in edges:
            back.setdefault(m, []).append((n, w))
    dist, queue = {n: float("inf") for n in graph}, [(0, "G")]
    dist["G"] = 0
    while queue:
        d, n = heapq.heappop(queue)
        if d == dist[n]:
            for m, w in back.get(n, []):
                if d + w < dist[m]:
                    dist[m] = d + w
                    heapq.heappush(queue, (d + w, m))
    print(title)
    print("path:", " -> ".join(path), "| cost:", g, "| recheck:", check)
    print("trace:", " ".join(f"{n}({g},{hh},{f})" for n, g, hh, f in order))
    print("expanded:", expanded, "| count:", len(expanded))
    print("admissible:", all(h[n] <= dist[n] for n in h),
          "| consistent:", all(h[u] <= w + h[v] for u, edges in graph.items() for v, w in edges))

show("A*", heuristic)
print()
show("UCS", {n: 0 for n in graph})
print()

bad = dict(heuristic)
bad["C"] = 10
show("Overestimate h(C) = 10", bad)
print()

g, p, _ = astar(graph, heuristic, "G", "G")
print("start is goal -> cost:", g, "path:", p)
g, p, _ = astar({n: [] for n in graph}, heuristic, "S", "G")
print("no route -> cost:", g, "path:", p)
