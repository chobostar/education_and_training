# python3


def lcs2(first_sequence, second_sequence):
    assert len(first_sequence) <= 100
    assert len(second_sequence) <= 100

    len_f = len(first_sequence)+1
    len_s = len(second_sequence)+1
    d = [[0 for _ in range(len_s)] for _ in range(len_f)]
    for i in range(1,len_f):
        for j in range(1,len_s):
            if first_sequence[i-1] == second_sequence[j-1]:
                d[i][j] = d[i-1][j-1]+1
            else:
                d[i][j] = max(d[i-1][j], d[i][j-1])
    return d[len_f-1][len_s-1]


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    assert len(a) == n

    m = int(input())
    b = list(map(int, input().split()))
    assert len(b) == m

    print(lcs2(a, b))
