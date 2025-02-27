import streamlit as st
import json
import plotly.graph_objects as go

st.set_page_config(layout="wide")

with open('income_statement.json', 'r') as f:
    income_data = json.load(f)

with open('key_metric.json', 'r') as f:
    key_metric_data = json.load(f)

dates = [entry['date'] for entry in income_data]
revenue = [entry['revenue'] / 1000000 for entry in income_data]
gross_profit_margin = [entry['grossProfit'] for entry in income_data]
net_margin = [entry['netIncome'] for entry in income_data]

dividend_yield = [metric['dividendYield'] for metric in key_metric_data]
current_ratio = [metric['currentRatio'] for metric in key_metric_data]
debt_ratio = [metric['debtToEquity'] for metric in key_metric_data]
pe_ratio = [metric['peRatio'] for metric in key_metric_data]
ps_ratio = [metric['priceToSalesRatio'] for metric in key_metric_data]

dates.reverse()
revenue.reverse()
gross_profit_margin.reverse()
net_margin.reverse()
dividend_yield.reverse()
current_ratio.reverse()
debt_ratio.reverse()
pe_ratio.reverse()
ps_ratio.reverse()

symbol = 'NVDA'

st.title(f"{symbol} Financial Metrics Dashboard")

metrics = {
    "Revenue (Millions)": revenue,
    "Gross Profit Margin": gross_profit_margin,
    "Net Margin": net_margin,
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
