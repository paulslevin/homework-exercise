import pytest

from sssm import Trade
from sssm import tradeDirection

test_params = [
    ('NOT INT', 10, tradeDirection.SELL),
    (10, 'NOT INT', tradeDirection.BUY),
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


def test_Trade_constructor_types():
    with pytest.raises(TypeError):
        Trade(10, 10, 'NOT IN ENUM')


