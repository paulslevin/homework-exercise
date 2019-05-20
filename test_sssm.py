import datetime

import pytest

from sssm import *

test_params = [
    (10, 10, 'NOT IN ENUM'),
    (10.5, 10, tradeDirection.BUY),
    (10, 10.5, tradeDirection.SELL),
    ('NOT INT', 10, tradeDirection.SELL),
    (10, 'NOT INT', tradeDirection.BUY),
]

@pytest.mark.parametrize("quantity,price,indicator", test_params)
def test_Trade_constructor_types(quantity, price, indicator):
    with pytest.raises(TypeError):
        Trade(quantity, price, indicator)


test_params = [
    (0, 10, tradeDirection.SELL),
    (10, 0, tradeDirection.BUY),
    (0, 0, tradeDirection.BUY),
    (-1, 10, tradeDirection.SELL),
    (10, -1, tradeDirection.BUY),
    (-1, -1, tradeDirection.BUY)
]

@pytest.mark.parametrize("quantity,price,indicator", test_params)
def test_Trade_constructor_values(quantity, price, indicator):
    with pytest.raises(ValueError):
        Trade(quantity, price, indicator)


def test_Trade_constructor_valid():
    Trade(10,10, tradeDirection.BUY)

def test_Trade_isYoungerThan_younger():
    trade = Trade(10, 10, tradeDirection.BUY)
    assert trade.isYoungerThan(10) == True

def test_Trade_isYoungerThan_older():
    trade = Trade(10, 10, tradeDirection.BUY)
    trade.timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=11)
    assert trade.isYoungerThan(10) == False

test_params = [
    (1000, 10, 10),
    ('ABC', 10.5, 10),
    ('ABC', 10, 10.5),
    ('ABC', '', 10),
    ('ABC', 10, '')
]

@pytest.mark.parametrize("stock_symbol,last_dividend,par_value", test_params)
def test_Stock_constructor_types(stock_symbol, last_dividend, par_value):
    with pytest.raises(TypeError):
        #  https://stackoverflow.com/a/17345619
        Stock.__abstractmethods__=set()
        Stock(stock_symbol, last_dividend, par_value)


test_params = [
    ('', 10, 10),
    ('ABCD', 10, 10),
    ('AB', 10, 10),
    ('ABC', -1, 10),
    ('ABC', 10, 0),
    ('ABC', 10, -1)
]

@pytest.mark.parametrize("stock_symbol,last_dividend,par_value", test_params)
def test_Stock_constructor_values(stock_symbol, last_dividend, par_value):
    with pytest.raises(ValueError):
        Stock.__abstractmethods__=set()
        Stock(stock_symbol, last_dividend, par_value)


test_params = [
    ('ABC', 0, 10),
    ('ABC', 10, 10)
]

@pytest.mark.parametrize("stock_symbol,last_dividend,par_value", test_params)
def test_Stock_constructor_valid(stock_symbol, last_dividend, par_value):
    Stock.__abstractmethods__=set()
    Stock(stock_symbol, last_dividend, par_value)


    
