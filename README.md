# HFT Risk Manager

A Python-based simulated trading and risk management system designed to explore core concepts in quantitative trading, market making, order execution, and pre-trade risk controls.

## Overview

This project simulates a simplified trading workflow by connecting market data generation, market-making quote generation, order execution, and risk validation into a modular Python application.

The goal is to understand how trading components interact and how risk controls can help prevent excessive position exposure and losses.

## Features

- **Market Simulation:** Generates simulated bid and ask prices, mid-prices, spreads, and available market liquidity.
- **Market Making:** Generates bid and ask quotes around the simulated market mid-price.
- **Order Execution:** Models marketable limit orders, full fills, partial fills, and unfilled orders based on available liquidity.
- **Risk Management:** Implements position limits, order-side validation, and P&L loss-threshold checks.
- **Trading Engine:** Integrates market simulation, quote generation, risk checks, and execution into a single workflow.
- **Automated Testing:** Uses `pytest` to validate market, execution, and risk-engine behavior.

## Architecture

```text
              Market Simulator
                     |
                     v
              Market Maker
             (Bid / Ask Quotes)
                     |
                     v
               Trading Engine
                     |
                     v
                 Risk Engine
             (Position Limits)
                     |
                     v
             Execution Simulator
                     |
                     v
             Execution Results
                     |
                     v
             Position Updates
```

The architecture separates responsibilities into independent modules, making the system easier to test, debug, and extend.

## Project Structure

```text
HFT-RiskManager/
├── market_simulator.py
├── market_maker.py
├── execution_simulator.py
├── risk_engine.py
├── trading_engine.py
├── monitoring.py
├── dashboard.py
├── logs/
│   └── trading.log
├── tests/
│   ├── test_market.py
│   ├── test_execution.py
│   └── test_risk.py
├── requirements.txt
└── README.md
```

## Tech Stack

- **Language:** Python
- **Testing:** pytest
- **Version Control:** Git and GitHub

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hrishabh3253/HFT-RiskManager.git
cd HFT-RiskManager
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the trading simulation

```bash
python trading_engine.py
```

### 4. Run the test suite

```bash
python -m pytest -v
```

The current test suite contains 19 passing tests covering market simulation, execution behavior, and risk-engine logic.

## Risk Management

The risk engine currently includes:

- Configurable maximum position limits.
- Validation of BUY and SELL order directions.
- Position updates based on filled quantities.
- P&L threshold checks.

These controls demonstrate basic pre-trade risk concepts. Further work is needed to fully integrate loss-limit enforcement with order execution and to implement complete portfolio P&L accounting.

## Current Limitations

This is an educational trading simulation, not a production-grade high-frequency trading system.

- Market data is simulated rather than sourced from a live exchange.
- Execution models marketable limit orders using available simulated liquidity.
- Passive quote matching against incoming market participants is not yet implemented.
- Complete cash accounting, realized and unrealized P&L, transaction fees, and mark-to-market valuation remain future improvements.
- The simulation does not model production exchange connectivity or real-world low-latency infrastructure.

## Future Improvements

- Implement a portfolio accounting module with cash, inventory, and mark-to-market P&L.
- Simulate incoming market orders interacting with resting market-maker quotes.
- Enforce risk limits consistently before every order is executed.
- Add order lifecycle tracking and richer execution logs.
- Build a monitoring dashboard for positions, P&L, fills, and risk-limit utilization.
- Explore execution latency, slippage, and more realistic market microstructure.

## Learning Objectives

This project explores:

- Bid-ask spreads and market-making fundamentals.
- Limit orders, liquidity, and partial execution.
- Inventory and position risk.
- P&L thresholds and risk controls.
- Modular software design and automated testing.

## Disclaimer

This project is for educational and research purposes only. It does not connect to a live exchange and is not intended to execute real trades or provide financial advice.

## Author

**Hrishabh Kumar**

[GitHub Profile](https://github.com/hrishabh3253)

---

*Built as a learning project to explore quantitative trading systems and risk management.*
