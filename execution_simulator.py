
def execute_order(order_id, side, price, quantity, market_event):
    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")

    if quantity <= 0:
        raise ValueError("quantity must be positive")

    if price <= 0:
        raise ValueError("price must be positive")

    # Read the current market's prices and available liquidity
    market_bid = market_event["bid"]
    market_ask = market_event["ask"]

    if side == "BUY":
        # A BUY limit order can execute at the market ask
        # only if our maximum price is high enough.
        executable = price >= market_ask
        available_qty = market_event["ask_qty"]

    else:
        # A SELL limit order can execute at the market bid
        # only if our minimum price is low enough.
        executable = price <= market_bid
        available_qty = market_event["bid_qty"]

    if executable:
        filled_qty = min(quantity, available_qty)
    else:
        filled_qty = 0

    remaining_qty = quantity - filled_qty

    if filled_qty == quantity:
        status = "Filled"
    elif filled_qty > 0:
        status = "Partial"
    else:
        status = "Unfilled"

    # Record the price available on the opposite side
    execution_price = (
        market_ask if side == "BUY" else market_bid
    ) if filled_qty > 0 else None

    print(
        f"Order {order_id} | {side} | Limit: {price:.2f} | "
        f"Status: {status} | Filled: {filled_qty} | "
        f"Remaining: {remaining_qty}"
    )

    return {
        "order_id": order_id,
        "side": side,
        "price": price,
        "quantity": quantity,
        "status": status,
        "filled_quantity": filled_qty,
        "remaining_quantity": remaining_qty,
        "execution_price": execution_price,
    }
