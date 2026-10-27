
from collections import deque
import time


class TradingMonitor:
    def __init__(self, max_orders_per_window=5, window_seconds=10):
        self.max_orders = max_orders_per_window
        self.window_seconds = window_seconds
        self.order_timestamps = deque()

    def record_order(self, order_id, status):
        now = time.time()

        # Keep only orders inside the monitoring window
        self.order_timestamps.append(now)

        while (
            self.order_timestamps
            and now - self.order_timestamps[0] > self.window_seconds
        ):
            self.order_timestamps.popleft()

        print(f"ORDER EVENT | ID: {order_id} | Status: {status}")

        if status == "REJECTED":
            print(f"ALERT | Order {order_id} was rejected by risk controls")

        if len(self.order_timestamps) > self.max_orders:
            print(
                "ALERT | Excessive order activity detected: "
                f"{len(self.order_timestamps)} orders in "
                f"{self.window_seconds} seconds"
            )


if __name__ == "__main__":
    monitor = TradingMonitor(
        max_orders_per_window=5,
        window_seconds=10
    )

    # Simulate a burst of order events
    for order_id in range(1, 9):
        monitor.record_order(order_id, "ACCEPTED")
        time.sleep(0.2)

    monitor.record_order(9, "REJECTED")
