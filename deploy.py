# -*- coding: utf-8 -*-
"""deploy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1duUpFilMdbui4_R1IZG8_t5LF6ff62no
"""
"""# **Pack**"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Analisis E-commerce")

# Fungsi untuk menghitung RFM
def calculate_rfm():
    # Menghitung recency
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    current_date = orders['order_purchase_timestamp'].max()

    orders_customers_df = pd.merge(orders_df[['order_id', 'customer_id', 'order_purchase_timestamp']], customers_df, on='customer_id', how='inner')
    recency_df = orders_customers_df.groupby('customer_unique_id').agg(
        last_purchase=('order_purchase_timestamp', 'max')
    ).reset_index()
    recency_df['recency'] = (current_date - recency_df['last_purchase']).dt.days

    # Menghitung frequency
    frequency_df = orders_customers_df.groupby('customer_unique_id').agg(
        frequency=('order_id', 'count')
    ).reset_index()

    # Menghitung monetary
    monetary_df = pd.merge(orders_customers_df[['order_id', 'customer_unique_id']], order_items_df[['order_id', 'price']], on='order_id', how='inner')
    monetary_df = monetary_df.groupby('customer_unique_id').agg(
        total_spent=('price', 'sum')
    ).reset_index()

    # Menggabungkan recency, frequency, dan monetary
    rfm_df = pd.merge(recency_df[['customer_unique_id', 'recency']], frequency_df[['customer_unique_id', 'frequency']], on='customer_unique_id')
    rfm_df = pd.merge(rfm_df, monetary_df[['customer_unique_id', 'total_spent']], on='customer_unique_id')

    return rfm_df

# Membuat heatmap korelasi
corr_rfm = rfm[['recency', 'frequency', 'monetary']].corr()

# Membuat visualisasi di Streamlit
st.title('RFM Correlation Heatmap')

plt.figure(figsize=(6, 4))
sns.heatmap(corr_rfm, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix for RFM')

# Tampilkan visualisasi heatmap menggunakan Streamlit
st.pyplot(plt)
