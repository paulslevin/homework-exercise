import datetime

import pytest

from sssm import Trade
from sssm import tradeDirection

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

def test_Trade_constructor_valid():
    Trade(10,10, tradeDirection.BUY)

def test_Trade_isYoungerThan_true():
    trade = Trade(10, 10, tradeDirection.BUY)
    assert trade.isYoungerThan(10) == True

def test_Trade_isYoungerThan_false():
    trade = Trade(10, 10, tradeDirection.BUY)
    trade.timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=11)
    assert trade.isYoungerThan(10) == False



