#!/usr/bin/python3

import sys, threading
from collections import deque

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**25)  # new thread will get stack of such size

def IsBinarySearchTree(tree):
  # Implement correct algorithm here
  if len(tree) == 0:
    return True
  q = deque()
  q.append((0,0))
  while len(q) > 0:
    node, parent = q.popleft()
    if node == -1:
      continue
    if node != 0:
      if tree[node][0] <= tree[parent][0] and (
        tree[node][1] != -1 and tree[tree[node][1]][0] > tree[parent][0]
        or tree[node][2] != -1 and tree[tree[node][2]][0] > tree[parent][0]):
        return False
      if tree[node][0] >= tree[parent][0] and (
        tree[node][1] != -1 and tree[tree[node][1]][0] < tree[parent][0]
        or tree[node][2] != -1 and tree[tree[node][2]][0] < tree[parent][0]):
        return False
    if tree[node][1] != -1 and tree[tree[node][1]][0] > tree[node][0] \
      or tree[node][2] != -1 and tree[tree[node][2]][0] < tree[node][0]:
      return False
    q.append((tree[node][1], node))
    q.append((tree[node][2], node))
  return True


def main():
  nodes = int(sys.stdin.readline().strip())
  tree = []
  for i in range(nodes):
    tree.append(list(map(int, sys.stdin.readline().strip().split())))
  if IsBinarySearchTree(tree):
    print("CORRECT")
  else:
    print("INCORRECT")

threading.Thread(target=main).start()
