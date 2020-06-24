#Uses python3

import sys

sys.setrecursionlimit(200000)


def get_reverse_adj(adj):
    radj = [[] for _ in range(len(adj))]
    for i in range(len(adj)):
        for a in adj[i]:
            radj[a].append(i)
    return radj


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
    visits.sort(key=lambda x: x[2], reverse=True)
    return visits


def number_of_strongly_connected_components(adj):
    radj = get_reverse_adj(adj)
    reverse_postorder = dfs(radj)
    visits = [[] for _ in range(len(adj))]
    scc_count = 0
    for v in reverse_postorder:
        if visits[v[0]]:
            continue
        explore(adj, visits, v[0], 0)
        scc_count += 1

    return scc_count


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(number_of_strongly_connected_components(adj))
