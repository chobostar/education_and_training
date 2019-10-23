# python3

from collections import namedtuple
from sys import stdin
from typing import List

Segment = namedtuple('Segment', 'start end')


def compute_optimal_points(segments: List[Segment]):
    n = len(segments)
    visited = [False] * n
    output_points = []
    sorted_segments = sorted(segments, key=lambda x: x.end)
    for i in range(n):
        if visited[i]:
            continue
        points = []
        for j in range(n):
            if visited[j]:
                continue
            if sorted_segments[i].start <= sorted_segments[j].start <= sorted_segments[i].end:
                points.append(sorted_segments[j].start)
            if sorted_segments[i].start <= sorted_segments[j].end <= sorted_segments[i].end:
                points.append(sorted_segments[j].end)
        local_max = -1
        best_point = 1000000000000
        for point in points:
            union = sum( not visited[k] and (sorted_segments[k].start <= point <= sorted_segments[k].end) for k in range(n))
            if local_max < union:
                local_max, best_point = union, point
            elif local_max == union and best_point < point:
                local_max, best_point = union, point

        for k in range(n):
            if (not visited[k]) and (sorted_segments[k].start <= best_point <= sorted_segments[k].end):
                visited[k] = True
        output_points.append(best_point)

    return output_points


if __name__ == '__main__':
    n, *data = map(int, stdin.read().split())
    input_segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    assert n == len(input_segments)
    output_points = compute_optimal_points(input_segments)
    print(len(output_points))
    print(" ".join(map(str, output_points)))
