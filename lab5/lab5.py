def search(leaves, d, i, is_max, alpha, beta, count, prune):
    if d == 3:
        count[0] += 1
        return leaves[i]
    best = float('-inf') if is_max else float('inf')
    for k in range(2):
        v = search(leaves, d + 1, 2 * i + k, not is_max, alpha, beta, count, prune)
        if is_max:
            best = max(best, v)
            alpha = max(alpha, best)
        else:
            best = min(best, v)
            beta = min(beta, best)
        if prune and alpha >= beta:
            break
    return best


def check(got, want):
    print("PASS" if got == want else "FAIL", got)


def run(name, leaves):
    a = [0]
    b = [0]
    x = search(leaves, 0, 0, True, float('-inf'), float('inf'), a, False)
    y = search(leaves, 0, 0, True, float('-inf'), float('inf'), b, True)
    print(name, "| minimax", x, "leaves", a[0], "| alphabeta", y, "leaves", b[0])
    check(x, 5)
    check(y, 5)


print("Task 1 hand trace")
print("leaves 3 5 | 2 9 | 0 7 | 0 0")
print("MAX    5 9 7 0")
print("MIN    5 0")
print("root   5")

print("Task 2 leaf counters")
run("given tree  ", [3, 5, 2, 9, 0, 7, 0, 0])

print("Task 3 reorder branches, same answer")
run("better order", [3, 5, 6, 9, 1, 2, 0, -1])
run("swap halves ", [1, 2, 0, -1, 3, 5, 6, 9])

print("edge case, all leaves equal")
c = [0]
check(search([4] * 8, 0, 0, True, float('-inf'), float('inf'), c, True), 4)
