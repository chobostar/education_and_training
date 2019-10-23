# python3
from typing import List


def lcs3(first_sequence, second_sequence, third_sequence):
    assert len(first_sequence) <= 100
    assert len(second_sequence) <= 100
    assert len(third_sequence) <= 100

    len_f = len(first_sequence)+1
    len_s = len(second_sequence)+1
    len_t = len(third_sequence)+1
    d = [[[0 for _ in range(len_t)] for _ in range(len_s)] for _ in range(len_f)]
    for i in range(1, len_f):
        for j in range(1, len_s):
            for k in range(1, len_t):
                if first_sequence[i-1] == second_sequence[j-1] == third_sequence[k-1]:
                    d[i][j][k] = d[i-1][j-1][k-1]+1
                else:
                    d[i][j][k] = max(d[i-1][j][k], d[i][j-1][k], d[i][j][k-1])
    return  d[len_f-1][len_s-1][len_t-1]
# 8 3 2 1 7 3
# 8 2 1 3 8 10 7
# 6 8 3 1 4 7

if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    assert len(a) == n

    m = int(input())
    b = list(map(int, input().split()))
    assert len(b) == m

    q = int(input())
    c = list(map(int, input().split()))
    assert len(c) == q

    print(lcs3(a, b, c))
