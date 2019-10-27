# python3

import sys, threading
from collections import deque


sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class TreeOrders:
    def read(self):
        self.n = int(sys.stdin.readline())
        self.key = [0 for i in range(self.n)]
        self.left = [0 for i in range(self.n)]
        self.right = [0 for i in range(self.n)]
        for i in range(self.n):
            [a, b, c] = map(int, sys.stdin.readline().split())
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c

    def inOrder(self):
        #deep first
        self.result = []
        self.inOrderTraversal(0)
        return self.result

    def inOrderTraversal(self, node_num):
        if node_num == -1:
            return
        self.inOrderTraversal(self.left[node_num])
        self.result.append(self.key[node_num])
        self.inOrderTraversal(self.right[node_num])

    def preOrder(self):
        self.result = []
        self.preOrderTraversal(0)
        return self.result

    def preOrderTraversal(self, node_num):
        if node_num == -1:
            return
        self.result.append(self.key[node_num])
        self.preOrderTraversal(self.left[node_num])
        self.preOrderTraversal(self.right[node_num])

    def postOrder(self):
        self.result = []
        self.postOrderTraversal(0)
        return self.result

    def postOrderTraversal(self, node_num):
        if node_num == -1:
            return
        self.postOrderTraversal(self.left[node_num])
        self.postOrderTraversal(self.right[node_num])
        self.result.append(self.key[node_num])


def main():
    tree = TreeOrders()
    tree.read()
    print(" ".join(str(x) for x in tree.inOrder()))
    print(" ".join(str(x) for x in tree.preOrder()))
    print(" ".join(str(x) for x in tree.postOrder()))

threading.Thread(target=main).start()
