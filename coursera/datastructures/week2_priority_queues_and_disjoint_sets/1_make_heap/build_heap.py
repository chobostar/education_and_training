# python3

swaps = []


class Heap(object):
    def __init__(self, data):
        self.data = data
        self.swaps = []
        self.size = len(data)

    def left_child(self, i):
        return 2*(i+1)-1

    def right_child(self, i):
        return 2*(i+1)

    def parent(self, i):
        return (i-1) // 2

    def sift_down(self, i):
        max_index = i
        left = self.left_child(i)
        if left < self.size and self.data[left] < self.data[max_index]:
            max_index = left
        right = self.right_child(i)
        if right < self.size and self.data[right] < self.data[max_index]:
            max_index = right
        if i != max_index:
            self.data[i], self.data[max_index] = self.data[max_index], self.data[i]
            self.swaps.append((i, max_index))
            self.sift_down(max_index)

    def build_heap(self):
        for i in reversed(range(0, self.size//2 + 1)):
            self.sift_down(i)


def build_heap(data):
    """Build a heap from ``data`` inplace.

    Returns a sequence of swaps performed by the algorithm.
    """
    # The following naive implementation just sorts the given sequence
    # using selection sort algorithm and saves the resulting sequence
    # of swaps. This turns the given array into a heap, but in the worst
    # case gives a quadratic number of swaps.
    #
    heap = Heap(data)
    heap.build_heap()
    return heap.swaps


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    swaps = build_heap(data)

    print(len(swaps))
    for i, j in swaps:
        print(i, j)


if __name__ == "__main__":
    main()
