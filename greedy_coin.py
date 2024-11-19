#!/usr/bin/env python
# make file executable by: chmod +x greedy_coin.py
# ./greedy_coin.py --help
import click


def greedy_coin(change):
    """
    return a dictionary with the coin type as the key and numbers for a given value
    """

    print(f"your change for {change}:")
    coins = [0.25, 10, 0.05, 0.01]
    coin_lookup = {}

    for coin in coins:
        while change >= coin:
            change -= coin
            if str(coin) in coin_lookup.keys():
                coin_lookup[str(coin)] += 1
            else:
                coin_lookup[str(coin)] = 1

    for coin, val in coin_lookup.items():
        if coin_lookup[coin] > 0:
            print(f"{coin}: {val}")
    return coin_lookup


@click.command()
@click.argument("change", type=float)
def main(change):
    """
    Return the minimum number of coins for a given change
    Example: greedy_coin.py 0.99
    """
    greedy_coin(change)


if __name__ == "__main__":
    main()
