# Simple Trader

This repository contains a quantitative trading strategy implementation, **SuperAlphaStrategy**, using
the [Nautilus Trader](https://github.com/nautechsystems/nautilus_trader) framework.

## Overview

The `SuperAlphaStrategy` is a rules-based trading strategy that utilizes the following technical indicators:

- **Exponential Moving Average (EMA) 9**
- **MACD (Moving Average Convergence/Divergence) 8-17-9**
- **Stochastics Oscillator 14-5**

Buy and sell signals are generated when all indicators and price conditions are met.

## Logic

- **Buys** when:
    - Not already in a position
    - MACD > MACD Signal
    - Closing price > EMA-9
    - Stochastics %K > %D

- **Sells** when:
    - Already in a position
    - MACD < MACD Signal
    - Closing price < EMA(9)
    - Stochastics %K < %D

## Setup

### Pre-requisites

- [uv](https://github.com/astral-sh/uv) package manager
- Python 3.13

### Installation

1. Install uv (if not already installed):

```bash
pip install uv
```

2. Activate a Python virtual environment:

```bash
source .venv/bin/activate
```

3. Install dependencies in your virtual Python environment:

```bash
uv sync
```

4. Running the project

```bash
python src/main.py
```

## Usage

- Monitor logs to watch trading decisions and performance.

## Important Notes

- Ensure Interactive Brokers Gateway/TWS is running and configured correctly
- Make sure you have the required permissions for live trading

## Disclaimer

This project is for educational and informational purposes only. It does not constitute investment advice or a
solicitation to buy or sell any financial instrument. Trading in financial markets involves significant risk, and you
should consult with a qualified financial advisor before making any investment decisions. The authors and contributors
assume no responsibility for any losses or damages incurred as a result of using this strategy. Use at your own risk.





