
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="HFT Command Center",
    page_icon="📈",
    layout="wide"
)

# ---------- CONFIGURATION ----------
MAX_POSITION = 500
MAX_LOSS = 5000
ORDER_QTY = 20
FEE_PER_UNIT = 0.02

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #0b1020;
}
[data-testid="stMetric"] {
    background: #151e30;
    border: 1px solid #29354a;
    padding: 15px;
    border-radius: 12px;
}
[data-testid="stMetricLabel"] {
    color: #9caec5;
}
.block-container {
    padding-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ---------- INITIALIZE SIMULATION ----------
def initialize():
    st.session_state.market_price = 1000.00
    st.session_state.position = 0
    st.session_state.cash = 0.0
    st.session_state.realized_pnl = 0.0
    st.session_state.fees = 0.0
    st.session_state.orders = []
    st.session_state.history = []
    st.session_state.alerts = []
    st.session_state.order_id = 0
    st.session_state.tick = 0


if "market_price" not in st.session_state:
    initialize()


def simulate_tick():
    s = st.session_state

    # Move market price
    movement = random.choice([-0.10, -0.05, 0, 0.05, 0.10])
    s.market_price = round(s.market_price + movement, 2)
    s.tick += 1

    price = s.market_price
    bid = round(price - 0.05, 2)
    ask = round(price + 0.05, 2)

    # Randomly decide whether to submit a buy or sell order
    side = random.choice(["BUY", "SELL"])
    quantity = ORDER_QTY

    proposed_position = (
        s.position + quantity
        if side == "BUY"
        else s.position - quantity
    )

    status = "REJECTED"
    filled = 0

    # Risk check BEFORE execution
    total_pnl = (
        s.realized_pnl
        + s.position * price
        + s.cash
        - s.fees
    )

    if abs(proposed_position) > MAX_POSITION:
        s.alerts.append(
            f"Tick {s.tick}: {side} rejected — position limit"
        )
    elif total_pnl <= -MAX_LOSS:
        s.alerts.append(
            f"Tick {s.tick}: {side} rejected — loss limit"
        )
    else:
        # Simplified simulated executable liquidity.
        # BUY orders execute against the ask;
        # SELL orders execute against the bid.
        available_qty = random.randint(0, 30)
        filled = min(quantity, available_qty)

        if filled == quantity:
            status = "FILLED"
        elif filled > 0:
            status = "PARTIAL"
        else:
            status = "UNFILLED"

        if filled > 0:
            execution_price = ask if side == "BUY" else bid

            # Update cash and inventory using actual simulated fills
            if side == "BUY":
                s.cash -= execution_price * filled
                s.position += filled
            else:
                s.cash += execution_price * filled
                s.position -= filled

            s.fees += filled * FEE_PER_UNIT

    s.order_id += 1

    s.orders.append({
        "Order ID": s.order_id,
        "Side": side,
        "Price": ask if side == "BUY" else bid,
        "Quantity": quantity,
        "Filled": filled,
        "Remaining": quantity - filled,
        "Status": status
    })

    # Mark-to-market accounting
    market_value = s.position * price
    unrealized_and_realized_pnl = (
        s.cash + market_value - s.fees
    )

    s.history.append({
        "Tick": s.tick,
        "Market Price": price,
        "Position": s.position,
        "Cash": round(s.cash, 2),
        "Fees": round(s.fees, 2),
        "Total P&L": round(unrealized_and_realized_pnl, 2)
    })


# ---------- HEADER ----------
header1, header2 = st.columns([3, 1])

with header1:
    st.title("⚡ HFT COMMAND CENTER")
    st.caption("Market simulation • Execution • Risk • Performance")

with header2:
    st.markdown("### 🟢 PAPER MODE")
    st.caption("Simulated data only")


# ---------- CONTROLS ----------
st.subheader("Simulation Controls")

c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    if st.button("▶ Run 1 Tick", use_container_width=True):
        simulate_tick()
        st.rerun()

with c2:
    if st.button("⏩ Run 10 Ticks", use_container_width=True):
        for _ in range(10):
            simulate_tick()
        st.rerun()

with c3:
    if st.button("↻ Reset Simulation", use_container_width=True):
        initialize()
        st.rerun()


# ---------- METRICS ----------
s = st.session_state
price = s.market_price

total_pnl = s.cash + s.position * price - s.fees

orders = s.orders
filled_orders = [
    o for o in orders if o["Filled"] > 0
]
total_submitted_qty = sum(o["Quantity"] for o in orders)
total_filled_qty = sum(o["Filled"] for o in orders)

fill_rate = (
    100 * total_filled_qty / total_submitted_qty
    if total_submitted_qty else 0
)

rejected_count = sum(
    o["Status"] == "REJECTED" for o in orders
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total P&L", f"₹{total_pnl:,.2f}")
m2.metric("Net Position", f"{s.position:+,}")
m3.metric("Market Price", f"₹{price:,.2f}")
m4.metric("Fill Rate", f"{fill_rate:.1f}%")

m5, m6, m7, m8 = st.columns(4)

m5.metric("Orders Submitted", len(orders))
m6.metric("Filled Quantity", total_filled_qty)
m7.metric("Risk Rejections", rejected_count)
m8.metric("Trading Fees", f"₹{s.fees:,.2f}")


# ---------- CHARTS ----------
left, right = st.columns([1.6, 1])

with left:
    st.subheader("📈 Market Price")
    if s.history:
        hist = pd.DataFrame(s.history).set_index("Tick")
        st.line_chart(hist[["Market Price"]], height=260)
    else:
        st.info("Run a tick to begin collecting market data.")

with right:
    st.subheader("💹 Equity / P&L Curve")
    if s.history:
        hist = pd.DataFrame(s.history).set_index("Tick")
        st.area_chart(hist[["Total P&L"]], height=260)
    else:
        st.info("P&L will appear after the first tick.")


# ---------- POSITIONS & RISK ----------
st.subheader("🛡️ Position and Risk Monitor")

r1, r2 = st.columns(2)

with r1:
    position_usage = min(
        abs(s.position) / MAX_POSITION, 1.0
    )
    st.write(f"Position: **{s.position:+} / ±{MAX_POSITION}**")
    st.progress(position_usage, text="Position limit utilization")

with r2:
    loss_usage = min(max(-total_pnl / MAX_LOSS, 0), 1.0)
    st.write(f"Loss limit: **₹{MAX_LOSS:,.0f}**")
    st.progress(loss_usage, text="Loss limit utilization")

if abs(s.position) >= MAX_POSITION:
    st.error("Position limit reached. Further exposure-increasing orders may be rejected.")
elif total_pnl <= -MAX_LOSS:
    st.error("Maximum loss limit reached.")
else:
    st.success("Risk checks: no configured limit currently breached.")


# ---------- ORDER BOOK ----------
st.subheader("📚 Simulated Market Snapshot")

st.table(pd.DataFrame([
    {
        "Side": "ASK",
        "Price": round(price + 0.05, 2),
        "Quantity": random.randint(50, 200)
    },
    {
        "Side": "BID",
        "Price": round(price - 0.05, 2),
        "Quantity": random.randint(50, 200)
    }
]))


# ---------- ORDERS ----------
st.subheader("📋 Order Blotter")

if orders:
    st.dataframe(
        pd.DataFrame(orders[::-1]),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No orders submitted yet.")


# ---------- ALERTS ----------
st.subheader("🚨 Risk & System Alerts")

if s.alerts:
    for alert in s.alerts[::-1][:10]:
        st.warning(alert)
else:
    st.success("No risk rejection alerts recorded.")


# ---------- DISCLAIMER ----------
st.caption(
    "Educational simulation only. Fill liquidity, prices, fees, and "
    "risk behaviour are simplified and are not representative of a "
    "real exchange or production HFT system."
)
