#Uses python3

import sys
import queue

def bipartite(adj):
    #write your code here
    all = queue.Queue()
    q = queue.Queue()
    color = [0 for _ in range(len(adj)) ]
    visited = 0
    limit = len(color)
    for i in range(limit):
        all.put(i)
    while visited < limit:
        v = -1
        while not all.empty():
            v = all.get()
            if color[v] != 0:
                continue
            else:
                break
        if v == -1:
            return 0
        q.put(v)
        visited += 1
        color[v] = 1
        while not q.empty():
            next = q.get()
            for v in adj[next]:
                if color[v] == 0:
                    color[v] = -1 * color[next]
                    visited += 1
                    q.put(v)
                elif color[v] == color[next]:
                    return 0
    return 1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(bipartite(adj))
