# python3

from collections import namedtuple
from typing import List

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])


class Heap(object):
    def __init__(self, data: List):
        self.data = data
        self.size = len(data)
        self.build_heap()

    def left_child(self, i):
        return 2*(i+1)-1

    def right_child(self, i):
        return 2*(i+1)

    def parent(self, i):
        return (i-1) // 2

    def sift_up(self, i):
        while i > 0 and self.data[self.parent(i)] > self.data[i]:
            self.data[self.parent(i)], self.data[i] = self.data[i], self.data[self.parent(i)]
            i = self.parent(i)

    def insert(self, p):
        self.size += 1
        self.data.append(p)
        self.sift_up(self.size-1)

    def extract_top(self):
        result = self.data[0]
        self.data[0] = self.data[self.size-1]
        self.size -= 1
        self.data.pop()
        self.sift_down(0)
        return result

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
            self.sift_down(max_index)

    def build_heap(self):
        for i in reversed(range(0, self.size//2 + 1)):
            self.sift_down(i)


def assign_jobs(n_workers, jobs):
    heap = Heap([(0,i) for i in range(n_workers)])
    result = []
    for job in jobs:
        next_free_time, next_worker = heap.extract_top()
        result.append(AssignedJob(next_worker, next_free_time))
        heap.insert((next_free_time+job, next_worker))
    return result


def assign_jobs_naive(n_workers, jobs):
    # TODO: replace this code with a faster algorithm.
    result = []
    next_free_time = [0] * n_workers
    for job in jobs:
        next_worker = min(range(n_workers), key=lambda w: next_free_time[w])
        result.append(AssignedJob(next_worker, next_free_time[next_worker]))
        next_free_time[next_worker] += job

    return result


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
