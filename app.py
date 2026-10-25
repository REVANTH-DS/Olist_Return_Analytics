import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="E-Commerce Return Analytics", layout="wide")
st.title("🛒 E-Commerce Product Return Rate & Refund Leakage Dashboard")

# Load Data
@st.cache_data
def load_data():
    df_returns = pd.read_csv('olist_processed_returns.csv')
    df_clusters = pd.read_csv('customer_clusters.csv')
    df_merged = df_returns.merge(df_clusters[['customer_id', 'Cluster_ID']], on='customer_id', how='left')
    return df_merged

df = load_data()

# Calculations
total_leakage = df[df['is_returned'] == 1]['total_payment'].sum()
freight_loss = df[df['is_returned'] == 1]['freight_value'].sum()
return_rate = (df['is_returned'].mean()) * 100

# Top KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Financial Leakage", f"${total_leakage:,.2f}")
col2.metric("Overall Return Rate", f"{return_rate:.2f}%")
col3.metric("Freight Loss on Returns", f"${freight_loss:,.2f}")

st.markdown("---")

# Visualizations Row 1
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Leakage Categories")
    top_cat = df[df['is_returned'] == 1].groupby('product_category')['total_payment'].sum().nlargest(10).reset_index()
    fig_bar = px.bar(top_cat, x='total_payment', y='product_category', orientation='h',
                     labels={'total_payment': 'Leakage ($)', 'product_category': 'Category'},
                     color='total_payment', color_continuous_scale='Reds')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Customer Cluster Breakdown")
    cluster_counts = df['Cluster_ID'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster_ID', 'Count']
    fig_pie = px.pie(cluster_counts, names='Cluster_ID', values='Count', hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Visualizations Row 2
st.subheader("Logistics Root Cause: Payment Method vs Return Rate")
payment_stats = df.groupby('primary_payment_type')['is_returned'].mean().reset_index()
payment_stats['return_rate_pct'] = payment_stats['is_returned'] * 100
fig_pay = px.bar(payment_stats, x='primary_payment_type', y='return_rate_pct',
                 labels={'primary_payment_type': 'Payment Type', 'return_rate_pct': 'Return Rate (%)'},
                 color='return_rate_pct', color_continuous_scale='Oranges')
st.plotly_chart(fig_pay, use_container_width=True)