import sys

# sys.version_info >= (3,6)

import enum
import abc
import datetime

class tradeDirection(enum.Enum):
        BUY = 0
        SELL = 1

class Trade:

    def __init__(self, quantity: int, price: int, indicator: tradeDirection) -> None:
        # @TODO: input validation

        self.quantity = quantity
        self.indicator = indicator
        self.price = price
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)


    def isYoungerThan(self, max_age_seconds: int) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - self.timestamp).total_seconds() <= max_age_seconds

class Stock(abc.ABC):

    # 15 minutes in seconds.
    _VWSP_max_age = 60 * 15

    def __init__(self, stock_symbol: str, last_dividend: int, par_value: int) -> None:
        # @TODO: input validation?

        self.stock_symbol = stock_symbol
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.trades = []

    @abc.abstractmethod
    def calculateDividendYield(self, price: int) -> float:
        pass

    def calculatePERatio(self, price: int) -> float:
        # @TODO: input validation

        if (self.last_dividend == 0):
            return 0.0

        return price / self.last_dividend

    def calculateVWSP(self) -> float:
        pass

    def buy(self, quantity: int, price: int) -> None:
        self.trades.append(Trade(quantity, price, tradeDirection.BUY))

    def sell(self, quantity: int, price: int) -> None:
        self.trades.append(Trade(quantity, price, tradeDirection.SELL))

    @abc.abstractmethod
    def _getName(self) -> str:
        pass

    def __str__(self) -> str:
        return self._getName()


class CommonStock(Stock):

    def _getName(self) -> str:
        return 'Common'

    def calculateDividendYield(self, price: int) -> float:
        # @TODO: input validation
        return self.last_dividend / price


class PreferredStock(Stock):

    def __init__(self, stock_symbol: str, last_dividend: int, par_value: int, fixed_dividend: int) -> None:
        super().__init__(stock_symbol, last_dividend, par_value)

        # @TODO: additional input validation.
        self.fixed_dividend = fixed_dividend

    def _getName(self) -> str:
        return 'Preferred'

    def calculateDividendYield(self, price: int) -> float:
        # @TODO: input validation.
        return (self.fixed_dividend * self.par_value) / price

x = CommonStock('TEA', 0, 100)
print(x.calculatePERatio(10))
print(x.calculateDividendYield(10))
print('---')

y = CommonStock('POP', 8, 100)
print(y.calculatePERatio(10))
print(y.calculateDividendYield(10))
print('---')

z = PreferredStock('GIN', 8, 100, 2)
print(z.calculatePERatio(10))
print(z.calculateDividendYield(10))


