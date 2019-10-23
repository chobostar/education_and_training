# python3

from sys import stdin
import random


def sort(items):
    less = []
    equal = []
    greater = []

    if len(items) > 1:
        pivot = random.choice(items)
        for x in items:
            if x['value'] < pivot['value']:
                less.append(x)
            elif x['value'] == pivot['value']:
                equal.append(x)
            elif x['value'] > pivot['value']:
                greater.append(x)
        return sort(greater)+equal+sort(less)
    else:
        return items


def maximum_loot_value(capacity, weights, prices):
    # assert 0 <= capacity <= 2 * 10 ** 6
    # assert len(weights) == len(prices)
    # assert 1 <= len(weights) <= 10 ** 3
    # assert all(0 < w <= 2 * 10 ** 6 for w in weights)
    # assert all(0 <= p <= 2 * 10 ** 6 for p in prices)

    items = [{'price': prices[i], 'weight': weights[i], 'value': prices[i]/weights[i]} for i in range(len(prices))]
    items_sorted = sort(items)
    result = 0
    for item in items_sorted:
        if capacity == 0:
            break
        if capacity > item['weight']:
            capacity -= item['weight']
            result += item['price']
        else:
            result += capacity/item['weight']*item['price']
            capacity = 0
    return result


if __name__ == "__main__":
    data = list(map(int, stdin.read().split()))
    n, input_capacity = data[0:2]
    input_prices = data[2:(2 * n + 2):2]
    input_weights = data[3:(2 * n + 2):2]
    opt_value = maximum_loot_value(input_capacity, input_weights, input_prices)
    print("{:.10f}".format(opt_value))
