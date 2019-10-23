# python3


def last_digit_of_fibonacci_number_naive(n):
    assert 0 <= n <= 10 ** 6

    if n <= 1:
        return n

    return (last_digit_of_fibonacci_number_naive(n - 1) + last_digit_of_fibonacci_number_naive(n - 2)) % 10


def last_digit_of_fibonacci_number(n):
    if n <= 1:
        return n
    if n == 2:
        return 1
    f_n_1 = 1
    f_n = 1
    for i in range(n-2):
        f_n_2 = f_n_1
        f_n_1 = f_n
        f_n = (f_n_1 + f_n_2) % 10
    return f_n


if __name__ == '__main__':
    input_n = int(input())
    print(last_digit_of_fibonacci_number(input_n))
