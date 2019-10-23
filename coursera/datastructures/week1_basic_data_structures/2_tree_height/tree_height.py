# python3

import sys
import threading


def get_height(childs, vertex):
    if len(childs[vertex]) == 0:
        return 1
    local_heights = []
    for i in range(len(childs[vertex])):
        local_heights.append(get_height(childs, childs[vertex][i]))
    return max(local_heights) + 1


def compute_height(n, parents):
    # Replace this code with a faster implementation
    childs = [[] for _ in range(n)]
    root = None
    for i in range(n):
        if parents[i] == -1:
            root = i
        else:
            childs[parents[i]].append(i)
    return get_height(childs, root)


def main():
    n = int(input())
    parents = list(map(int, input().split()))
    print(compute_height(n, parents))


if __name__ == "__main__":
    sys.setrecursionlimit(10**7)  # max depth of recursion
    threading.stack_size(2**27)   # new thread will get stack of such size
    threading.Thread(target=main).start()

#5
#-1 0 4 0 3


# In Python, the default limit on recursion depth is rather low,
# so raise it here for this problem. Note that to take advantage
# of bigger stack, we have to launch the computation in a new thread.
