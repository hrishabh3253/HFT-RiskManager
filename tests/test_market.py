
from market_simulator import generate_market_event


def test_market_event_has_required_fields():
    event = generate_market_event(1)

    required_fields = {
        "event_id",
        "mid_price",
        "bid",
        "ask",
        "spread",
        "bid_qty",
        "ask_qty",
    }

    assert required_fields.issubset(event.keys())


def test_bid_is_below_ask():
    event = generate_market_event(2)

    assert event["bid"] < event["ask"]


def test_spread_matches_bid_and_ask():
    event = generate_market_event(3)

    assert round(event["ask"] - event["bid"], 2) == event["spread"]


def test_market_quantities_are_positive():
    event = generate_market_event(4)

    assert event["bid_qty"] > 0
    assert event["ask_qty"] > 0
