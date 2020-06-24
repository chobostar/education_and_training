#Uses python3

import sys


def explore(adj, visits, vertex, num):
    visits[vertex].append(num)
    num += 1
    for a in adj[vertex]:
        if visits[a] and len(visits[a]) < 2:
            return 1
        result = explore(adj, visits, a, num)
        if result == 1:
            return 1
    visits[vertex].append(num)


def acyclic(adj):
    visits = [[] for _ in range(len(adj))]
    num = 0
    for i in range(len(adj)):
        if visits[i]:
            continue
        result = explore(adj, visits, i, num)
        if result == 1:
            return 1
    return 0


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(acyclic(adj))
