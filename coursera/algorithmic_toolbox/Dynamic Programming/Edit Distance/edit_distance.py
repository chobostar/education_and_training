# python3


def edit_distance(first_string, second_string):
    n = len(first_string)+1
    m = len(second_string)+1
    d = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(m):
        d[0][i] = i
    for i in range(n):
        d[i][0] = i
    for i in range(1, n):
        for j in range(1, m):
            d[i][j] = min([
                d[i][j-1]+1,
                d[i-1][j]+1,
                d[i-1][j-1]+1 if first_string[i-1] != second_string[j-1] else d[i-1][j-1]
            ])
    return d[n-1][m-1]


if __name__ == "__main__":
    print(edit_distance(input(), input()))
