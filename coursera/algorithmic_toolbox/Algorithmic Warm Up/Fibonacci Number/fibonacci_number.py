# python3


def fibonacci_number_naive(n):
    assert 0 <= n <= 40

    if n <= 1:
        return n

    return fibonacci_number_naive(n - 1) + fibonacci_number_naive(n - 2)


def fibonacci_number_optimal(n):
    if n <= 1:
        return n
    if n == 2:
        return 1
    f_n_1 = 1
    f_n = 1
    for i in range(n-2):
        f_n_2 = f_n_1
        f_n_1 = f_n
        f_n = f_n_1 + f_n_2
    return f_n


def fibonacci_number(n):
    return fibonacci_number_optimal(n)


if __name__ == '__main__':
    input_n = int(input())
    print(fibonacci_number(input_n))
