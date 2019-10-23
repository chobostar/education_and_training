# python3


def fibonacci_number_again_naive(n, m):
    assert 0 <= n <= 10 ** 18 and 2 <= m <= 10 ** 3

    if n <= 1:
        return n

    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, (previous + current) % m

    return current


def find_period(n, m):
    if n <= 2:
        return n
    f_n_1, f_n = 1, 1
    period_len = 0
    for i in range(n-2):
        f_n_2, f_n_1 = f_n_1, f_n
        f_n = (f_n_1 + f_n_2) % m
        period_len += 1
        if f_n_2 == 0 and f_n_1 == 1 and f_n == 1:
            return period_len

    return n


def fibonacci_number_again(n, m):
    assert 0 <= n <= 10 ** 18 and 2 <= m <= 10 ** 3

    period_len = find_period(n, m)

    return fibonacci_number_again_naive(n % period_len if period_len < n else n, m)


if __name__ == '__main__':
    input_n, input_m = map(int, input().split())
    print(fibonacci_number_again(input_n, input_m))
