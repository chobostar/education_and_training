#Uses python3

import sys


def explore(adj, visits, vertex, num):
    visits[vertex].append(vertex)
    visits[vertex].append(num)
    num += 1
    for a in adj[vertex]:
        if visits[a]:
            continue
        num = explore(adj, visits, a, num)
    visits[vertex].append(num)
    num += 1
    return num


def dfs(adj):
    visits = [[] for _ in range(len(adj))]
    num = 0
    for i in range(len(adj)):
        if visits[i]:
            continue
        if adj[i]:
            num = explore(adj, visits, i, num)
    for i in range(len(visits)):
        if not visits[i]:
            visits[i].append(i)
            visits[i].append(num)
            num += 1
            visits[i].append(num)
            num += 1
    visits.sort(key=lambda x: x[2])
    order = [entry[0] for entry in visits]
    return order


def toposort(adj):
    order = dfs(adj)
    order.reverse()
    return order


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')

