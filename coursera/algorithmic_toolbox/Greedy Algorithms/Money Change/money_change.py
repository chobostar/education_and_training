# python3


def money_change(money):
    coins = 0
    if (money // 10) > 0:
        coins += money // 10
        money = money % 10
    if (money // 5) > 0:
        coins += money // 5
        money = money % 5
    coins += money
    return coins


if __name__ == '__main__':
    input_money = int(input())
    print(money_change(input_money))
