#python3
import sys
import math

class StackWithMax():
    def __init__(self):
        self.__stack = []
        self.__max = []

    def Push(self, a):
        self.__stack.append(a)
        if len(self.__max) == 0 or self.Max() <= a:
            self.__max.append(a)

    def Pop(self):
        assert(len(self.__stack))
        a = self.__stack.pop()
        if self.__max[len(self.__max)-1] == a:
            self.__max.pop()
        return a

    def Max(self):
        assert(len(self.__stack))
        return self.__max[len(self.__max)-1]


if __name__ == '__main__':
    stack = StackWithMax()

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        query = sys.stdin.readline().split()

        if query[0] == "push":
            stack.Push(int(query[1]))
        elif query[0] == "pop":
            stack.Pop()
        elif query[0] == "max":
            print(stack.Max())
        else:
            assert(0)
