
import pytest
from execution_simulator import execute_order


@pytest.fixture
def market():
    return {
        "bid": 999.90,
        "ask": 1000.10,
        "bid_qty": 30,
        "ask_qty": 40,
    }


def test_buy_fills_from_available_ask(market):
    result = execute_order(1, "BUY", 1000.10, 100, market)

    assert result["filled_quantity"] == 40
    assert result["remaining_quantity"] == 60
    assert result["status"] == "Partial"
    assert result["execution_price"] == 1000.10


def test_sell_fills_from_available_bid(market):
    result = execute_order(2, "SELL", 999.90, 20, market)

    assert result["filled_quantity"] == 20
    assert result["remaining_quantity"] == 0
    assert result["status"] == "Filled"
    assert result["execution_price"] == 999.90


def test_non_marketable_buy_does_not_fill(market):
    result = execute_order(3, "BUY", 1000.00, 50, market)

    assert result["filled_quantity"] == 0
    assert result["remaining_quantity"] == 50
    assert result["status"] == "Unfilled"


def test_non_marketable_sell_does_not_fill(market):
    result = execute_order(4, "SELL", 1000.00, 50, market)

    assert result["filled_quantity"] == 0
    assert result["remaining_quantity"] == 50
    assert result["status"] == "Unfilled"


def test_order_cannot_fill_more_than_available(market):
    result = execute_order(5, "BUY", 1000.10, 10, market)

    assert result["filled_quantity"] == 10
    assert result["remaining_quantity"] == 0


@pytest.mark.parametrize("quantity", [0, -1])
def test_quantity_must_be_positive(market, quantity):
    with pytest.raises(ValueError):
        execute_order(6, "BUY", 1000.10, quantity, market)
