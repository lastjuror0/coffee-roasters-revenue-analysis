import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import duckdb
import seaborn as sns
from scipy import stats
import matplotlib.cm as cm
from matplotlib.colors import Normalize

st.set_page_config(layout="wide")

df = pd.read_csv('Afficionado Coffee Roasters.csv')
df['revenue'] = df['transaction_qty'] * df['unit_price']

### Filters
st.sidebar.header("Filters")

category_options = ['All'] + sorted(df['product_category'].unique().tolist())
selected_category = st.sidebar.selectbox('Product Category', category_options)

if selected_category == 'All':
    filtered_df = df
else:
    filtered_df = df[df['product_category'] == selected_category]

type_options = ['All'] + sorted(filtered_df['product_type'].unique().tolist())
selected_type = st.sidebar.selectbox('Product Type', type_options)

if selected_type != 'All':
    filtered_df = filtered_df[filtered_df['product_type'] == selected_type]

store_options = sorted(df['store_location'].unique().tolist())
selected_stores = st.sidebar.multiselect('Store Location', store_options, default=store_options)

if selected_stores:
    filtered_df = filtered_df[filtered_df['store_location'].isin(selected_stores)]

### Header
st.markdown("## ☕ Coffee Analytics Dashboard")
st.caption("This dashboard explores product performance across a coffee shop's menu using transactional data from 2025. The goal is to understand which products drive the business, how revenue is distributed, and where the menu's strengths and weaknesses lie.")


### KPIs
total_revenue = round(filtered_df['revenue'].sum(), 2)
total_units = int(filtered_df['transaction_qty'].sum())
avg_revenue_per_product = round(filtered_df['revenue'].sum() / filtered_df['product_id'].nunique(), 2)

revenue_ratio = duckdb.query("""
    With cte as (
        Select product_id, sum(revenue) / (select sum(revenue) From filtered_df) as revenue_ratio
        From filtered_df
        Group by product_id
        Order by revenue_ratio desc
        Limit 10)
    Select round(sum(revenue_ratio) * 100, 2) as revenue_ratio
    From cte
""").fetchall()[0][0]

# Display KPIs in containers
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    with st.container(border=True):
        st.metric(
            label="💰 Total Revenue", 
            value=f"${total_revenue:,.2f}")

with kpi2:
    with st.container(border=True):
        st.metric(
            label="📦 Units Sold", 
            value=f"{total_units:,}")

with kpi3:
    with st.container(border=True):
        st.metric(
            label="📈 Avg Revenue/Product", 
            value=f"${avg_revenue_per_product:,.2f}")

with kpi4:
    with st.container(border=True):
        st.metric(
            label="🎯 Top 10 Concentration", 
            value=f"{revenue_ratio}%")

st.markdown("#### Revenue Analysis")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        category_revenue = duckdb.query("""
            Select product_category, round(sum(revenue), 2) as total_revenue
            from filtered_df
            Group By product_category
            order by total_revenue asc
        """).df()

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        norm = Normalize(vmin=0, vmax=category_revenue['total_revenue'].max())
        colors = cm.Oranges(norm(category_revenue['total_revenue']))

        ax.barh(category_revenue['product_category'], category_revenue['total_revenue'], color=colors)
        ax.set_title('Category Revenue Distribution', color='white',fontweight='bold')
        ax.set_xlabel('Total Revenue', color='white')
        ax.set_ylabel('', color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)

with col2:
    with st.container(border=True):
        type_revenue = duckdb.query("""
            Select product_type, round(sum(revenue), 2) as total_revenue
            from filtered_df
            Group By product_type
            order by total_revenue asc
            limit 15
        """).df()

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        norm = Normalize(vmin=0, vmax=type_revenue['total_revenue'].max())
        colors = cm.Oranges(norm(type_revenue['total_revenue']))

        ax.barh(type_revenue['product_type'], type_revenue['total_revenue'], color=colors)
        ax.set_title('Top 15 Revenue by Product Type', color='white',fontweight='bold')
        ax.set_xlabel('Total Revenue', color='white')
        ax.set_ylabel('', color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)


st.markdown("#### Product Performance Analysis")
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        revenue_by_product = duckdb.query("""
            Select product_id, round(sum(revenue), 2) as total_revenue
            from filtered_df
            group by product_id
            order by total_revenue desc
        """).df()

        revenue_by_product['cumulative_pct'] = (revenue_by_product['total_revenue'].cumsum() / revenue_by_product['total_revenue'].sum() * 100)

        fig, ax1 = plt.subplots(figsize=(8, 5))
        fig.patch.set_alpha(0)
        ax1.patch.set_alpha(0)

        norm = Normalize(vmin=0, vmax=revenue_by_product['total_revenue'].max())
        colors = cm.Oranges(norm(revenue_by_product['total_revenue']))

        ax1.bar(revenue_by_product['product_id'].astype(str), revenue_by_product['total_revenue'], color=colors)
        ax1.set_title('Pareto Chart - Revenue by Product', color='white',fontweight='bold')
        ax1.set_xlabel('Product ID', color='white')
        ax1.set_ylabel('Total Revenue', color='white')
        ax1.tick_params(colors='white')
        ax1.set_xticks([])

        ax2 = ax1.twinx()
        ax2.plot(revenue_by_product['product_id'].astype(str), revenue_by_product['cumulative_pct'], color='white', marker='o', markersize=3)
        ax2.axhline(80, color='orange', linestyle='--', label='80% threshold')
        ax2.set_ylabel('Cumulative Revenue %', color='white')
        ax2.tick_params(colors='white')
        ax2.legend(facecolor='#0e1117', labelcolor='white')
        st.pyplot(fig)

with col2:
    with st.container(border=True):
        scatter_df = duckdb.query("""
            Select product_id,
                sum(transaction_qty) as total_units,
                round(sum(revenue), 2) as total_revenue
            from filtered_df
            group by product_id
        """).df()

        fig, ax = plt.subplots(figsize=(11, 6))
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        norm = Normalize(vmin=0, vmax=scatter_df['total_revenue'].max())
        colors = cm.Oranges(norm(scatter_df['total_revenue']))

        ax.scatter(scatter_df['total_units'], scatter_df['total_revenue'],
                   c=colors, s=80, edgecolors='white', linewidths=0.5)

        # Correlation line
        m, b = np.polyfit(scatter_df['total_units'], scatter_df['total_revenue'], 1)
        x_line = np.linspace(scatter_df['total_units'].min(), scatter_df['total_units'].max(), 100)
        ax.plot(x_line, m * x_line + b, color='orange', linestyle='--', linewidth=1.5, label=f'r = {scatter_df["total_units"].corr(scatter_df["total_revenue"]):.2f}')

        ax.set_title('Popularity vs Revenue', color='white', fontweight='bold')
        ax.set_xlabel('Total Units Sold', color='white')
        ax.set_ylabel('Total Revenue', color='white')
        ax.tick_params(colors='white')
        ax.legend(facecolor='#0e1117', labelcolor='white')
        st.pyplot(fig)