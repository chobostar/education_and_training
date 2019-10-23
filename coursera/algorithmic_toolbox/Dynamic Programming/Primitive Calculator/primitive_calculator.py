# python3


def compute_operations(n):
    assert 1 <= n <= 10 ** 6
    answer = [0] * (n+1)
    steps = [0] * (n+1)
    for i in range(1, n+1):
        possibles = [answer[i-1]]
        local_step = [i-1]
        if i % 2 == 0:
            possibles.append(answer[i // 2])
            local_step.append(i//2)
        if i % 3 == 0:
            possibles.append(answer[i // 3])
            local_step.append(i//3)
        optimum = min(possibles)
        answer[i] = optimum + 1
        steps[i] = local_step[possibles.index(optimum)]
    output = []
    j = n
    while steps[j] != 0:
        output.append(j)
        j = steps[j]
    output.append(1)
    output.reverse()

    return output


if __name__ == '__main__':
    input_n = int(input())
    output_sequence = compute_operations(input_n)
    print(len(output_sequence) - 1)
    print(" ".join(map(str, output_sequence)))
