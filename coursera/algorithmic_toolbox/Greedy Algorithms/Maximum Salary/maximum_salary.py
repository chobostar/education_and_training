# python3

from itertools import permutations
import random


def if_greater(x, y: str) -> bool:
    return (x + y) > (y + x)


def sort(items):
    less = []
    equal = []
    greater = []

    if len(items) > 1:
        pivot = random.choice(items)
        for x in items:
            if not if_greater(x, pivot) and x != pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif if_greater(x, pivot):
                greater.append(x)
        return sort(greater)+equal+sort(less)
    else:
        return items


def largest_number_naive(numbers):
    numbers = list(map(str, numbers))

    largest = 0

    for permutation in permutations(numbers):
        largest = max(largest, int("".join(permutation)))

    return largest


def largest_number(numbers):
    sorted_numbers = sort([str(number) for number in numbers])
    result = ''.join(sorted_numbers)
    return int(result)


if __name__ == '__main__':
    n = int(input())
    input_numbers = input().split()
    assert len(input_numbers) == n
    print(largest_number(input_numbers))
