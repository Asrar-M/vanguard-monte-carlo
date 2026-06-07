import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Retirement Monte Carlo Simulator", layout="wide")

st.title("Retirement Monte Carlo Simulator")
st.markdown("Built using Vanguard's expected return assumptions and glide path philosophy.")

# --- Sidebar Inputs ---
st.sidebar.header("Your Parameters")

starting_age = st.sidebar.slider("Current Age", 18, 50, 22)
retirement_age = st.sidebar.slider("Retirement Age", 55, 75, 65)
end_age = st.sidebar.slider("Plan Until Age", 80, 100, 95)
starting_balance = st.sidebar.number_input("Starting Balance ($)", 0, 500000, 0, step=1000)

st.sidebar.subheader("Monthly Contributions by Decade")
contrib_20s = st.sidebar.slider("In Your 20s ($/mo)", 0, 2000, 300, step=50)
contrib_30s = st.sidebar.slider("In Your 30s ($/mo)", 0, 3000, 600, step=50)
contrib_40s = st.sidebar.slider("In Your 40s ($/mo)", 0, 5000, 1000, step=50)
contrib_50s = st.sidebar.slider("In Your 50s+ ($/mo)", 0, 6000, 1500, step=50)

num_simulations = st.sidebar.select_slider("Number of Simulations", [500, 1000, 2000], 1000)

# --- Return Assumptions ---
st.sidebar.subheader("Return Assumptions (Vanguard Defaults)")
stock_return = st.sidebar.slider("Expected Stock Return (%)", 3.0, 12.0, 6.5, step=0.1) / 100
bond_return = st.sidebar.slider("Expected Bond Return (%)", 1.0, 7.0, 3.5, step=0.1) / 100
stock_vol = st.sidebar.slider("Stock Volatility (%)", 5.0, 25.0, 17.0, step=0.5) / 100
bond_vol = st.sidebar.slider("Bond Volatility (%)", 1.0, 10.0, 6.0, step=0.5) / 100

# --- Helper Functions ---
def get_stock_allocation(age):
    if age < 40:
        return 0.90
    elif age < 55:
        return 0.75
    elif age < 65:
        return 0.60
    else:
        return 0.50

def get_monthly_contribution(age):
    if age < 30:
        return contrib_20s
    elif age < 40:
        return contrib_30s
    elif age < 55:
        return contrib_40s
    else:
        return contrib_50s

# --- Simulation Functions ---
def simulate_accumulation():
    all_paths = []
    accumulation_years = retirement_age - starting_age

    for _ in range(num_simulations):
        portfolio = starting_balance
        path = [portfolio]

        for year in range(accumulation_years):
            current_age = starting_age + year
            stock_alloc = get_stock_allocation(current_age)
            bond_alloc = 1 - stock_alloc

            stock_ret = np.random.normal(stock_return, stock_vol)
            bond_ret = np.random.normal(bond_return, bond_vol)
            portfolio_ret = (stock_alloc * stock_ret) + (bond_alloc * bond_ret)

            annual_contribution = get_monthly_contribution(current_age) * 12
            portfolio = portfolio * (1 + portfolio_ret) + annual_contribution
            path.append(portfolio)

        all_paths.append(path)
    return all_paths

def simulate_withdrawal(accumulation_paths):
    final_portfolios = [path[-1] for path in accumulation_paths]
    withdrawal_years = end_age - retirement_age
    all_paths = []
    success_count = 0

    for i in range(num_simulations):
        portfolio = final_portfolios[i]
        annual_withdrawal = portfolio * 0.04
        path = [portfolio]
        survived = True

        for year in range(withdrawal_years):
            current_age = retirement_age + year
            stock_alloc = get_stock_allocation(current_age)
            bond_alloc = 1 - stock_alloc

            stock_ret = np.random.normal(stock_return, stock_vol)
            bond_ret = np.random.normal(bond_return, bond_vol)
            portfolio_ret = (stock_alloc * stock_ret) + (bond_alloc * bond_ret)

            portfolio = portfolio * (1 + portfolio_ret) - annual_withdrawal

            if portfolio <= 0:
                path.append(0)
                survived = False
                break

            path.append(portfolio)

        if survived:
            success_count += 1
        all_paths.append(path)

    success_rate = (success_count / num_simulations) * 100
    return all_paths, success_rate, final_portfolios

# --- Run Simulation ---
with st.spinner("Running simulations..."):
    accumulation_paths = simulate_accumulation()
    withdrawal_paths, success_rate, final_portfolios = simulate_withdrawal(accumulation_paths)

# --- Summary Stats ---
final_array = np.array(final_portfolios) / 1e6

col1, col2, col3, col4 = st.columns(4)
col1.metric("Success Rate", f"{success_rate:.1f}%")
col2.metric("Median Portfolio at Retirement", f"${np.median(final_array):.2f}M")
col3.metric("10th Percentile", f"${np.percentile(final_array, 10):.2f}M")
col4.metric("90th Percentile", f"${np.percentile(final_array, 90):.2f}M")

# --- Chart ---
def plot_bands(accumulation_paths, withdrawal_paths, success_rate):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f'Monte Carlo Retirement Simulation | {num_simulations} Simulations | Vanguard Return Assumptions',
                 fontsize=12, fontweight='bold')

    acc_years = list(range(starting_age, retirement_age + 1))
    acc_array = np.array(accumulation_paths) / 1e6

    p10 = np.percentile(acc_array, 10, axis=0)
    p25 = np.percentile(acc_array, 25, axis=0)
    p50 = np.percentile(acc_array, 50, axis=0)
    p75 = np.percentile(acc_array, 75, axis=0)
    p90 = np.percentile(acc_array, 90, axis=0)

    ax1.fill_between(acc_years, p10, p90, alpha=0.15, color='steelblue', label='10th–90th percentile')
    ax1.fill_between(acc_years, p25, p75, alpha=0.30, color='steelblue', label='25th–75th percentile')
    ax1.plot(acc_years, p50, color='steelblue', linewidth=2.5, label='Median')
    ax1.plot(acc_years, p10, color='steelblue', linewidth=1, linestyle='--', alpha=0.5)
    ax1.set_title(f'Accumulation Phase (Age {starting_age}–{retirement_age})', fontweight='bold')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Portfolio Value ($M)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    with_years = list(range(retirement_age, end_age + 1))
    total_years = end_age - retirement_age + 1

    padded = []
    for path in withdrawal_paths:
        if len(path) < total_years:
            path = path + [0] * (total_years - len(path))
        padded.append(path)

    with_array = np.array(padded) / 1e6

    p10w = np.percentile(with_array, 10, axis=0)
    p25w = np.percentile(with_array, 25, axis=0)
    p50w = np.percentile(with_array, 50, axis=0)
    p75w = np.percentile(with_array, 75, axis=0)
    p90w = np.percentile(with_array, 90, axis=0)

    ax2.fill_between(with_years, p10w, p90w, alpha=0.15, color='seagreen', label='10th–90th percentile')
    ax2.fill_between(with_years, p25w, p75w, alpha=0.30, color='seagreen', label='25th–75th percentile')
    ax2.plot(with_years, p50w, color='seagreen', linewidth=2.5, label='Median Surviving Path')
    ax2.plot(with_years, p10w, color='tomato', linewidth=1.5, linestyle='--', label='10th percentile (worst realistic)')
    ax2.set_title(f'Withdrawal Phase (Age {retirement_age}–{end_age}) | Success Rate: {success_rate:.1f}%',
                  fontweight='bold')
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Portfolio Value ($M)')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

fig = plot_bands(accumulation_paths, withdrawal_paths, success_rate)
st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.caption("Return assumptions based on Vanguard Capital Markets Model (VCMM). "
           "This tool is for educational purposes only and does not constitute financial advice.")