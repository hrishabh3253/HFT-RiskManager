
from risk_engine import riskengine


def test_order_within_position_limit_is_approved():
    risk = riskengine(max_position=500)

    approved, message = risk.check_order("BUY", 300)

    assert approved is True
    assert message == "Order Approved"


def test_order_exceeding_position_limit_is_rejected():
    risk = riskengine(max_position=500)
    risk.update_position("BUY", 300)

    approved, message = risk.check_order("BUY", 250)

    assert approved is False
    assert message == "Position Limit Breached"


def test_sell_order_updates_position():
    risk = riskengine()

    risk.update_position("SELL", 100)

    assert risk.position == -100


def test_buy_order_updates_position():
    risk = riskengine()

    risk.update_position("BUY", 100)

    assert risk.position == 100


def test_invalid_order_side_is_rejected():
    risk = riskengine()

    approved, message = risk.check_order("HOLD", 100)

    assert approved is False
    assert message == "INVALID SIDE"


def test_loss_below_limit_is_allowed():
    risk = riskengine(max_loss=5000)

    approved, message = risk.check_loss(-3000)

    assert approved is True


def test_loss_at_limit_is_breached():
    risk = riskengine(max_loss=5000)

    approved, message = risk.check_loss(-5000)

    assert approved is False


def test_loss_above_limit_is_breached():
    risk = riskengine(max_loss=5000)

    approved, message = risk.check_loss(-5200)

    assert approved is False
