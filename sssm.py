# The name of this package makes it hard to understand its purpose.
# Something like super_simple_stocks.py is better than sssm.py

import enum
import abc
import datetime

# All Python classes should use UpperCamelCase
class TradeDirection(enum.Enum):
    BUY = 0
    SELL = 1

# You ended up doing the same price check over and over. might be a good
# idea to use a decorator to do this
def positive_price_check(f):
    def wrapper(*args, **kwargs):
        price = kwargs.get('price')
        if price <= 0:
            raise ValueError('Positive price must be provided.')
        return f(*args, **kwargs)
    return wrapper


# You don't really need to specify the type. Python allows polymorphism
class Trade:
    @positive_price_check
    def __init__(self, quantity, price, indicator):

        # Same here, this is unnecessary. If you try to create a Stock object
        # and pass in the wrong type, Python will already raise a TypeError
        # if you do something unexpected with it.

        # Explicit is better than implicit. Also no need to call int.
        if quantity <= 0:
            raise ValueError('Positive quantity must be provided.')

        self.quantity = quantity
        self.indicator = indicator
        self.price = price
        self.timestamp = datetime.datetime.now(datetime.timezone.utc)

    # Python methods should follow snake_case
    def is_younger_than(self, max_age_seconds: int) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - self.timestamp).total_seconds() <= max_age_seconds


class Stock(abc.ABC):
    # Strangely formatted compared to the other methods
    # What is VWSP?
    # VWSP should be lower case
    def __init__(self, stock_symbol, last_dividend, par_value, vwsp_max_age):

        # Better to use not equal comparison, and again be explicit
        if len(stock_symbol) != 3:
            raise ValueError('Stock symbol needs to be 3 characters.')

        if last_dividend < 0:
            raise ValueError('Last dividend must be non-negative.')

        if par_value <= 0:
            raise ValueError('Par value must be positive.')

        self.stock_symbol = stock_symbol
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.vwsp_max_age = vwsp_max_age
        self.trades = []

    # Snake case
    @abc.abstractmethod
    def calculate_dividend_yield(self, price):
        pass

    @positive_price_check
    def calculate_per_ratio(self, price):

        # better to just use not than do a zero comparison
        if not self.last_dividend:
            return 0.0

        return price / self.last_dividend

    def calculate_vwsp(self) -> float:
        total_quantity = 0
        total_value = 0

        for trade in self.trades:
            if trade.is_younger_than(self.vwsp_max_age):
                total_value += trade.price * trade.quantity
                total_quantity += trade.quantity

        # No trades or all trades too old.
        if not total_quantity:
            return 0.0

        return total_value / total_quantity

    def buy(self, quantity, price):
        self.trades.append(Trade(quantity, price, TradeDirection.BUY))

    def sell(self, quantity, price):
        # I have made an assumption that there is no need to check that the quantity of shares
        # are available to sell given the exercise offers no state of this kind for us to bootstrap from.
        self.trades.append(Trade(quantity, price, TradeDirection.SELL))


class CommonStock(Stock):
    @positive_price_check
    def calculate_dividend_yield(self, price):
        return self.last_dividend / price


class PreferredStock(Stock):
    def __init__(self, stock_symbol, last_dividend, par_value, fixed_dividend):
        super().__init__(stock_symbol, last_dividend, par_value)

        if not 0 <= fixed_dividend <= 100:
            raise ValueError('fixed_dividend must be in the range [0, 100]')

        self.fixed_dividend = fixed_dividend

    @positive_price_check
    def calculate_dividend_yield(self, price):
        return ((self.fixed_dividend / 100.0) * self.par_value) / price


class StockIndex:
    def __init__(self, name, stocks):
        self.name = name
        self.stocks = {stock.stock_symbol: stock for stock in stocks}

    def get_Stock(self, stock_symbol):
        return self.stocks[stock_symbol]

    def calculate_all_share_index(self):
        # For real systems you would import scipy or similar but there is value in keeping
        # this homework exercise free of external dependencies where possible.

        total = 1
        for stock in self.stocks.values():
            total *= stock.calculate_vwsp()

        return total ** (1 / len(self.stocks))
