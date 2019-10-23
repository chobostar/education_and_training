# python3
import collections


class StackWithMax:
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

    def Size(self):
        return len(self.__stack)

    def __repr__(self):
        return str(self.__stack)


class Queue:
    def __init__(self):
        self.__inbox = StackWithMax()
        self.__outbox = StackWithMax()

    def Push(self, a):
        self.__inbox.Push(a)

    def Pop(self):
        if self.__outbox.Size() == 0:
            while self.__inbox.Size() > 0:
                self.__outbox.Push(self.__inbox.Pop())
        return self.__outbox.Pop()

    def Max(self):
        if self.__outbox.Size() > 0 and self.__inbox.Size() > 0:
            return max(self.__inbox.Max(), self.__outbox.Max())
        elif self.__outbox.Size() > 0:
            return self.__outbox.Max()
        else:
            return self.__inbox.Max()



def max_sliding_window_naive(sequence, m):
    maximums = []
    for i in range(len(sequence) - m + 1):
        maximums.append(max(sequence[i:i + m]))

    return maximums


def max_sliding_window(sequence, m):
    queue = Queue()
    maximums = []

    for i in range(m):
        queue.Push(sequence[i])
    maximums.append(queue.Max())

    for i in range(m, len(sequence)):
        queue.Pop()
        queue.Push(sequence[i])
        maximums.append(queue.Max())

    return maximums


if __name__ == '__main__':
    n = int(input())
    input_sequence = [int(i) for i in input().split()]
    assert len(input_sequence) == n
    window_size = int(input())

    print(*max_sliding_window(input_sequence, window_size))

