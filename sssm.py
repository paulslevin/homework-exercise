import enum
import abc
import datetime


class tradeDirection(enum.Enum):
    BUY = 0
    SELL = 1


class Trade:
    def __init__(self, quantity: int, price: int, indicator: tradeDirection) -> None:

        if not isinstance(indicator, tradeDirection):
            raise TypeError

        if not isinstance(quantity, int) or not isinstance(price, int):
            raise TypeError

        if int(quantity) <= 0 or int(price) <= 0:
            raise ValueError

        self.quantity = quantity
        self.indicator = indicator
        self.price = price
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)

    def isYoungerThan(self, max_age_seconds: int) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - self.timestamp).total_seconds() <= max_age_seconds


class Stock(abc.ABC):
    def __init__(
        self,
        stock_symbol: str,
        last_dividend: int,
        par_value: int,
        VWSP_max_age: int = 900,
    ) -> None:

        if not isinstance(stock_symbol, str):
            raise TypeError

        if not isinstance(last_dividend, int) or not isinstance(par_value, int):
            raise TypeError

        if not len(stock_symbol) == 3:
            raise ValueError

        if int(last_dividend) < 0 or int(par_value) <= 0:
            raise ValueError

        self.stock_symbol = stock_symbol
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.VWSP_max_age = VWSP_max_age
        self.trades = []

    @abc.abstractmethod
    def calculateDividendYield(self, price: int) -> float:
        pass

    def calculatePERatio(self, price: int) -> float:

        if not isinstance(price, int):
            raise TypeError

        if price <= 0:
            raise ValueError

        if self.last_dividend == 0:
            return 0.0

        return price / self.last_dividend

    def calculateVWSP(self) -> float:
        total_quantity = 0
        total_value = 0

        for trade in self.trades:
            if trade.isYoungerThan(self.VWSP_max_age):
                total_value += trade.price * trade.quantity
                total_quantity += trade.quantity

        # No trades or all trades too old.
        if total_quantity == 0:
            return 0.0

        return total_value / total_quantity

    def buy(self, quantity: int, price: int) -> None:
        self.trades.append(Trade(quantity, price, tradeDirection.BUY))

    def sell(self, quantity: int, price: int) -> None:
        # I have made an assumption that there is no need to check that the quantity of shares
        # are available to sell given the exercise offers no state of this kind for us to bootstrap from.
        self.trades.append(Trade(quantity, price, tradeDirection.SELL))


class CommonStock(Stock):
    def calculateDividendYield(self, price: int) -> float:
        if not isinstance(price, int):
            raise TypeError

        if price <= 0:
            raise ValueError

        return self.last_dividend / price


class PreferredStock(Stock):
    def __init__(
        self,
        stock_symbol: str,
        last_dividend: int,
        par_value: int,
        fixed_dividend: float,
    ) -> None:
        super().__init__(stock_symbol, last_dividend, par_value)

        if not isinstance(fixed_dividend, float):
            raise TypeError

        if fixed_dividend < 0 or fixed_dividend > 100:
            raise ValueError

        self.fixed_dividend = fixed_dividend

    def calculateDividendYield(self, price: int) -> float:

        if not isinstance(price, int):
            raise TypeError

        if price <= 0:
            raise ValueError

        return ((self.fixed_dividend / 100.0) * self.par_value) / price


class StockIndex:
    def __init__(self, name: str, stocks: list) -> None:
        self.name = name
        self.stocks = {stock.stock_symbol: stock for stock in stocks}

    def getStock(self, stock_symbol: str) -> Stock:
        return self.stocks[stock_symbol]

    def calculateAllShareIndex(self) -> int:
        # For real systems you would import scipy or similar but there is value in keeping
        # this homework exercise free of external dependencies where possible.

        total = 1
        for stock in self.stocks.values():
            total *= stock.calculateVWSP()

        return total ** (1 / len(self.stocks))
