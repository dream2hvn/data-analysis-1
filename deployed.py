# -*- coding: utf-8 -*-
"""deployed.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HrWbeuarj6T4gAc6b15lu6woa7GsLevn
"""

from google.colab import drive
drive.mount('/content/drive')

pip install streamlit

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca setiap dataset ke dalam DataFrame pandas
customers = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_customers_dataset.csv')
geolocation = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_geolocation_dataset.csv')
order_items = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_order_items_dataset.csv')
order_payments = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_order_payments_dataset.csv')
order_reviews = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_order_reviews_dataset.csv')
orders = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_orders_dataset.csv')
products = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_products_dataset.csv')
sellers = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/olist_sellers_dataset.csv')
product_category_translation = pd.read_csv('/content/drive/MyDrive/DATA ANALISIS/product_category_name_translation.csv')

# Title for the dashboard
st.title("Olist E-commerce Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a page:", ['Overview', 'Order Analysis', 'Product Analysis', 'Customer Analysis'])

# Overview page
if options == 'Overview':
    st.header("Dataset Overview")
    st.write("Customers dataset")
    st.dataframe(customers.head())
    st.write("Orders dataset")
    st.dataframe(orders.head())

    # Display summary statistics for orders
    st.write("Order Summary")
    st.write(orders.describe())

# Order Analysis page
if options == 'Order Analysis':
    st.header("Order Analysis")

    # Plot number of orders by status
    st.subheader("Order Status Distribution")
    order_status_counts = orders['order_status'].value_counts()
    fig, ax = plt.subplots()
    order_status_counts.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Plot number of orders over time
    st.subheader("Orders Over Time")
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders_by_date = orders.groupby(orders['order_purchase_timestamp'].dt.date).size()
    fig, ax = plt.subplots()
    orders_by_date.plot(ax=ax)
    st.pyplot(fig)

# Product Analysis page
if options == 'Product Analysis':
    st.header("Product Analysis")

    # Merge products with category translations
    products_merged = pd.merge(products, category_translation, on='product_category_name', how='left')

    # Display top categories by number of products
    top_categories = products_merged['product_category_name_english'].value_counts().head(10)
    st.subheader("Top Product Categories")
    fig, ax = plt.subplots()
    top_categories.plot(kind='bar', ax=ax)
    st.pyplot(fig)

# Customer Analysis page
if options == 'Customer Analysis':
    st.header("Customer Analysis")

    # Display top 10 customer locations by number of orders
    top_customer_locations = customers['customer_city'].value_counts().head(10)
    st.subheader("Top Customer Locations")
    fig, ax = plt.subplots()
    top_customer_locations.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Display distribution of customer states
    st.subheader("Customer State Distribution")
    customer_states = customers['customer_state'].value_counts()
    fig, ax = plt.subplots()
    customer_states.plot(kind='bar', ax=ax)
    st.pyplot(fig)

# Footer
st.sidebar.info("This dashboard is powered by Streamlit and Olist data.")