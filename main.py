import sys
import sssm

if (sys.version_info.major != 3) or (sys.version_info.minor != 6):
    print("Warning this program was written with python 3.6.7-final-0")
    print("Current version: " + str(sys.version_info))


stocks = [
    sssm.CommonStock("TEA", 0, 100),
    sssm.CommonStock("POP", 8, 100),
    sssm.CommonStock("ALE", 23, 60),
    sssm.PreferredStock("GIN", 8, 100, 2.0),
    sssm.CommonStock("JOE", 13, 250),
]

index = sssm.StockIndex("Global Beverage Corporation Exchange", stocks)

while True:

    print(
        """
        1 - Calculate the dividend yield given: [stock symbol, price]
        2 - Calculate the P/E ratio given [stock symbol, price]
        3 - Buy shares [stock symbol, quantity of shares, price]
        4 - Sell shares [stock symbol, quantity of shares, price]
        5 - Calculate Volume Weighted Stock Price [stock symbol]
        6 - Calculate All Share Index
        7 - Exit
    """
    )

    top_level_command = input("\t:")

    if top_level_command == "1":
        stock_symbol = input("\t\tstock symbol: ")
        price = input("\t\tprice: ")

        try:
            dividend_yield = index.getStock(stock_symbol).calculateDividendYield(
                int(price)
            )
            print("\t\t\tDividend yield: " + str(dividend_yield))
            continue
        except KeyError:
            print("\t\t\tUnknown stock symbol.")
            continue
        except ValueError or TypeError:
            print("\t\t\tPrice must be a positive integer.")
            continue

        # This version of Python (3.6) doesn't support continue in a finally block else I would use it.
        # See: https://stackoverflow.com/a/10544962

    if top_level_command == "2":
        stock_symbol = input("\t\tstock symbol: ")
        price = input("\t\tprice: ")

        try:
            pe_ratio = index.getStock(stock_symbol).calculatePERatio(int(price))
            print("\t\t\tP/E Ratio: " + str(pe_ratio))
            continue
        except KeyError:
            print("\t\t\tUnknown stock symbol.")
            continue
        except ValueError or TypeError:
            print("\t\t\tPrice must be a positive integer.")
            continue

    if top_level_command == "3":
        stock_symbol = input("\t\tstock symbol: ")
        quantity = input("\t\tquantity of shares: ")
        price = input("\t\tprice: ")

        try:
            index.getStock(stock_symbol).buy(int(quantity), int(price))
            print(
                "\t\t\tYou successfully bought {quantity} {stock_symbol} shares at {price} pennies".format(
                    quantity=quantity, stock_symbol=stock_symbol, price=price
                )
            )
            continue
        except KeyError:
            print("\t\t\tUnknown stock symbol.")
            continue
        except ValueError or TypeError:
            print("\t\t\tPrice and quantity must be a positive integers.")
            continue

    if top_level_command == "4":
        stock_symbol = input("\t\tstock symbol: ")
        quantity = input("\t\tquantity of shares: ")
        price = input("\t\tprice: ")

        try:
            index.getStock(stock_symbol).sell(int(quantity), int(price))
            print(
                "\t\t\tYou successfully sold {quantity} {stock_symbol} shares at {price} pennies".format(
                    quantity=quantity, stock_symbol=stock_symbol, price=price
                )
            )
            continue
        except KeyError:
            print("\t\t\tUnknown stock symbol.")
            continue
        except ValueError or TypeError:
            print("\t\t\tPrice and quantity must be a positive integers.")
            continue

    if top_level_command == "5":
        stock_symbol = input("\t\tstock symbol: ")

        try:
            print("\t\t\tVWSP: " + str(index.getStock(stock_symbol).calculateVWSP()))
            continue
        except KeyError:
            print("\t\t\tUnknown stock symbol.")
            continue

    if top_level_command == "6":
        print(
            "\t\t\t"
            + index.name
            + " all share index: "
            + str(index.calculateAllShareIndex())
        )
        continue

    if top_level_command == "7":
        break
    else:
        print("Top level command not supported.")
