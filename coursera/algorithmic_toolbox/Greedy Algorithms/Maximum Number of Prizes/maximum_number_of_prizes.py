# python3
import math


def compute_optimal_summands(n):
    assert 1 <= n <= 10 ** 9

    k = int((-1 + math.sqrt((n*8)+1)) // 2)
    summands = [i+1 for i in range(k-1)]
    summands.append(n - sum(summands))

    return summands


if __name__ == '__main__':
    input_n = int(input())
    output_summands = compute_optimal_summands(input_n)
    print(len(output_summands))
    print(" ".join(map(str, output_summands)))
