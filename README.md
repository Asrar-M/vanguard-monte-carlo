# Retirement Monte Carlo Simulator

An interactive retirement planning tool built in Python and Streamlit that models 
portfolio growth and retirement sustainability using Monte Carlo simulation.

**Live App:** https://vanguard-monte-carlo-fou7oo9xxbygsdvtai2qjb.streamlit.app/

---

## What It Does

The simulator runs 1,000 market scenarios to project retirement outcomes across two phases:

- **Accumulation Phase (Age 22 → 65):** Models portfolio growth through tiered monthly 
  contributions and compounding returns, with allocation automatically shifting from 
  aggressive to conservative as retirement approaches
- **Withdrawal Phase (Age 65 → 95):** Models whether the portfolio survives 30 years 
  of retirement withdrawals using the 4% rule

Rather than assuming fixed returns, each simulation randomly samples annual returns 
from a normal distribution — reflecting real market volatility. The output shows a 
range of outcomes across percentiles, not a single projected number.

---

## Key Features

- 1,000 Monte Carlo simulations per run
- Vanguard glide path allocation strategy (90/10 stocks/bonds at 22 → 50/50 at retirement)
- Tiered monthly contributions by decade reflecting realistic income growth
- 4% withdrawal rule applied to each simulation's unique retirement portfolio value
- Percentile band visualization (10th, 25th, 50th, 75th, 90th)
- Interactive sliders for age, contributions, return assumptions, and simulation count
- Live metrics: success rate, median portfolio, 10th and 90th percentile outcomes

---

## Assumptions & Limitations

- Return assumptions based on Vanguard's Capital Markets Model (VCMM):
  - US Equities: 6.5% expected annual return, 17% volatility
  - Bonds: 3.5% expected annual return, 6% volatility
- Returns are inflation-adjusted (real returns), not nominal
- Does not account for Social Security income, which would improve success rates
- Does not model capital gains taxes during portfolio rebalancing
- Withdrawal amount is fixed at 4% of retirement portfolio value and does not 
  adjust for inflation during retirement
- Assumes consistent contributions with no career interruptions

---

## Glide Path Allocation

| Age Range | Stocks | Bonds |
|-----------|--------|-------|
| 22 – 39   | 90%    | 10%   |
| 40 – 54   | 75%    | 25%   |
| 55 – 64   | 60%    | 40%   |
| 65+       | 50%    | 50%   |

This mirrors Vanguard's Target Date Fund philosophy — higher equity exposure 
early for growth, gradually shifting to bonds for capital preservation as 
retirement approaches.

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## References

- Vanguard Capital Markets Model (VCMM) — Expected Returns for US Equities and Bonds
- Vanguard Target Retirement Funds — Glide Path Methodology
- Bengen, W.P. (1994). "Determining Withdrawal Rates Using Historical Data." Journal of Financial Planning
- Cooley, Hubbard & Walz (1998). "Retirement Savings: Choosing a Withdrawal Rate That Is Sustainable." (The Trinity Study)
- Damodaran, A. — Annual Returns on Stock, T.Bonds and T.Bills: 1928–Current
- randerson112358 (2025). "Will Your Portfolio Survive Retirement?" Medium.
- Moffitt, C. (2019). "Monte Carlo Simulation with Python." Practical Business Python.

---

*This tool is for educational purposes only and does not constitute financial advice.*