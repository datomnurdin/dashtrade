import streamlit as st
import json
import plotly.graph_objs as go
import pandas as pd

st.set_page_config(layout="wide")

# Load data
with open('income_statement.json', 'r') as f:
    income_data = json.load(f)

with open('key_metric.json', 'r') as f:
    key_metric_data = json.load(f)

markets = ["NYSE", "NASDAQ"]
tickers = ["NVDA", "AAPL", "TSLA", "AMZN"]

selected_market = st.selectbox("Select Market", markets)
selected_ticker = st.selectbox("Select Ticker", tickers)

# Extract financial data
dates = [entry['date'] for entry in income_data]
revenue = [entry['revenue'] / 1000000 for entry in income_data]
gross_profit_margin = [entry['grossProfit'] for entry in income_data]
net_margin = [entry['netIncome'] for entry in income_data]

dividend_yield = [metric['dividendYield'] for metric in key_metric_data]
current_ratio = [metric['currentRatio'] for metric in key_metric_data]
debt_ratio = [metric['debtToEquity'] for metric in key_metric_data]
pe_ratio = [metric['peRatio'] for metric in key_metric_data]
ps_ratio = [metric['priceToSalesRatio'] for metric in key_metric_data]

free_cash_flow = [cash_flow['freeCashFlow'] for cash_flow in cash_flow_statement]

# Reverse for chronological order
free_cash_flow.reverse()

# Reverse data for chronological order
dates.reverse()
revenue.reverse()
gross_profit_margin.reverse()
net_margin.reverse()
free_cash_flow.reverse()
dividend_yield.reverse()
current_ratio.reverse()
debt_ratio.reverse()
pe_ratio.reverse()
ps_ratio.reverse()

symbol = selected_ticker
st.title(f"{symbol} Financial Metrics Dashboard")

# Fair Value Calculation (Discounted Cash Flow)
def calculate_fair_value(key_metrics):
    df = pd.DataFrame(key_metrics)

    # Extract free cash flow per share for recent years
    fcf_ps = df["freeCashFlowPerShare"].values

    # Estimate growth rate based on historical data (CAGR method)
    years = len(fcf_ps)
    growth_rate = (fcf_ps[0] / fcf_ps[-1]) ** (1 / (years - 1)) - 1

    # Discount rate (WACC estimation, assumed at 10%)
    discount_rate = 0.10

    # Terminal growth rate (assumed at 4% for mature companies)
    terminal_growth_rate = 0.04

    # Forecast future cash flows for 5 years
    years_forecast = 5
    future_fcf = [fcf_ps[0] * (1 + growth_rate) ** i for i in range(1, years_forecast + 1)]

    # Calculate terminal value using perpetuity formula
    terminal_value = future_fcf[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)

    # Discount future cash flows to present value
    present_values = [fcf / (1 + discount_rate) ** (i + 1) for i, fcf in enumerate(future_fcf)]
    present_values.append(terminal_value / (1 + discount_rate) ** years_forecast)

    # Sum all present values to get fair value per share
    fair_value = sum(present_values)
    return fair_value

fair_value = calculate_fair_value(key_metric_data)
st.metric(label="Estimated Fair Value (DCF)", value=f"${fair_value}")

# Prepare charts
metrics = {
    "Revenue (Millions)": revenue,
    "Gross Profit Margin": gross_profit_margin,
    "Net Margin": net_margin,
    "Free Cash Flow": free_cash_flow,
    "Dividend Yield": dividend_yield,
    "Current Ratio": current_ratio,
    "Debt Ratio": debt_ratio,
    "P/E Ratio": pe_ratio,
    "P/S Ratio": ps_ratio,
}

cols = st.columns(2)

def create_chart(x, y, title):
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode='lines+markers', name=title)])
    fig.update_layout(title=title, xaxis=dict(title='Date'), yaxis=dict(title=title), template="plotly_dark", height=500)
    return fig

for i, (title, data) in enumerate(metrics.items()):
    with cols[i % 2]:
        st.plotly_chart(create_chart(dates, data, f'{symbol} {title} Over Time'), use_container_width=True)
