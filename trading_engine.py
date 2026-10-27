
from market_simulator import generate_market_event
from market_maker import generate_quotes
from execution_simulator import execute_order
from risk_engine import riskengine


def run_simulation(number_of_events=10):
    risk = riskengine(max_position=500, max_loss=5000)

    total_submitted = 0
    total_filled = 0

    for event_id in range(1, number_of_events + 1):
        print(f"\n{'=' * 45}")
        print(f"MARKET EVENT {event_id}")
        print("=" * 45)

        # 1. Generate market data
        event = generate_market_event(event_id)

        # 2. Generate our quotes
        quotes = generate_quotes(event)

        print(f"Market mid: {event['mid_price']:.2f}")
        print(
            f"Our bid: {quotes['our_bid']:.2f} | "
            f"Our ask: {quotes['our_ask']:.2f}"
        )

        # 3. Choose a simulated order
        side = "BUY" if event_id % 2 == 1 else "SELL"
        quantity = 20

        price = (
            quotes["our_bid"]
            if side == "BUY"
            else quotes["our_ask"]
        )

        approved, message = risk.check_order(side, quantity)
        print(f"Risk decision: {message}")

        if not approved:
            print("Order rejected. No execution attempted.")
            continue

        # 4. Simulate execution
        total_submitted += 1

        
        result = execute_order(
         order_id=event_id,
         side=side,
         price=price,
         quantity=quantity,
         market_event=event,
)


        filled_qty = result["filled_quantity"]
        total_filled += filled_qty

        # 5. Update position using actual filled quantity only
        risk.update_position(side, filled_qty)

        print(f"Updated position: {risk.position}")

    print(f"\n{'=' * 45}")
    print("SIMULATION SUMMARY")
    print("=" * 45)
    print(f"Orders submitted: {total_submitted}")
    print(f"Total quantity filled: {total_filled}")
    print(f"Final position: {risk.position}")


if __name__ == "__main__":
    run_simulation()
