#Uses python3

import sys
import queue

def distance(adj, s, t):
    #write your code here
    q = queue.Queue()
    inf = len(adj)+1
    distance = [inf for _ in range(len(adj)) ]
    q.put(s)
    distance[s] = 0
    while not q.empty():
        next = q.get()
        for v in adj[next]:
            if distance[v] == inf:
                distance[v] = distance[next] + 1
                q.put(v)
    return distance[t] if distance[t] < inf else -1


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
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1
    print(distance(adj, s, t))
