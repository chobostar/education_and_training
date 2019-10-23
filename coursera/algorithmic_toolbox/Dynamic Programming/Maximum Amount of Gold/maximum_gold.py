# python3

from sys import stdin


def maximum_gold(capacity, weights):
    len_w = len(weights)
    capacity += 1
    d =[[0 for _ in range(capacity)] for _ in range(len_w)]
    for j in range(capacity):
        if weights[0] < j:
            d[0][j] = weights[0]
    for i in range(1, len_w):
        for j in range(1, capacity):
            if weights[i] <= j:
                d[i][j] = max(d[i-1][j], d[i-1][j-weights[i]]+weights[i])
            else:
                d[i][j] = d[i-1][j]
    return d[len_w-1][capacity-1]


if __name__ == '__main__':
    input_capacity, n, *input_weights = list(map(int, stdin.read().split()))
    assert len(input_weights) == n

    print(maximum_gold(input_capacity, input_weights))
