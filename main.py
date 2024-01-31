import timeit
from tabulate import tabulate

COINS = [100, 99, 66, 33, 9, 6, 3, 1]


def find_coins_greedy(coins, amount):
    result = {}
    for coin in coins:
        if amount >= coin:
            result[coin] = amount // coin
            amount = amount % coin
    return result


def find_min_coins(coins, amount):
    result = [amount + 1] * (amount + 1)
    coins_results = [[] for _ in range(amount + 1)]

    result[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and result[i - coin] + 1 < result[i]:
                result[i] = result[i - coin] + 1
                coins_results[i] = coins_results[i - coin] + [coin]

    if result[amount] == amount + 1:
        return []

    coin_dict = {}
    for coin in coins_results[amount]:
        if coin in coin_dict:
            coin_dict[coin] += 1
        else:
            coin_dict[coin] = 1

    return coin_dict


def main():
    min_amount = 100
    max_amount = 200

    def compare_algorithms(coins, min_amount, max_amount):
        differing_results = []

        for amount in range(min_amount, max_amount + 1):
            greedy_result = find_coins_greedy(coins, amount)
            dp_result = find_min_coins(coins, amount)

            # Converting dp_result to the same format as greedy_result for comparison
            dp_result_converted = dict(sorted(dp_result.items(), reverse=True))

            if greedy_result != dp_result_converted:
                differing_results.append((amount, greedy_result, dp_result_converted))

        return differing_results

    differing_amounts = compare_algorithms(COINS, min_amount, max_amount)

    formatted_data = []
    for amount, greedy_result, dp_result in differing_amounts:
        formatted_data.append(
            [
                amount,
                ", ".join(f"{k}: {v}" for k, v in greedy_result.items()),
                ", ".join(f"{k}: {v}" for k, v in dp_result.items()),
            ]
        )

    table = tabulate(
        formatted_data,
        headers=["Сума", "Жадібний алгоритм", "Динамічне програмування"],
        tablefmt="grid",
    )

    print(table)

    greedy_time = timeit.timeit(
        f"for i in range({min_amount}, {max_amount} + 1): find_coins_greedy(COINS, i)",
        globals=globals(),
        number=1,
    )

    dp_time = timeit.timeit(
        f"for i in range({min_amount}, {max_amount} + 1): find_min_coins(COINS, i)",
        globals=globals(),
        number=1,
    )

    print("Час на жадібний алгоритм: ", greedy_time)
    print("Час на динамічне програмування: ", dp_time)


if __name__ == "__main__":
    main()
