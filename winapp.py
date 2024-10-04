# -*- coding: utf-8 -*-
"""winapp

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jLkMBqEcYu9kGdH7GQN7AHa24ml_MEOH
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Title
st.title('Simple Dashboard: Data Comparison')

# Load the data
data = pd.read_csv('all_data.csv')

# Convert 'shipping_limit_date' to datetime format for easier plotting
data['shipping_limit_date'] = pd.to_datetime(data['shipping_limit_date'], errors='coerce')

# Remove rows with NaT (not a valid datetime)
data = data.dropna(subset=['shipping_limit_date'])

# Sort data by date to ensure proper plotting
data = data.sort_values('shipping_limit_date')

# Streamlit app setup
st.title('1. Price and Freight Value Over Time')

# Line plot: Price and Freight Value Over Time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data['shipping_limit_date'], data['price'], label='Price', color='green', alpha=0.6)
ax.plot(data['shipping_limit_date'], data['freight_value'], label='Freight Value', color='red', alpha=0.6)
ax.set_title('Price and Freight Value Over Time')
ax.set_xlabel('Shipping Limit Date')
ax.set_ylabel('Value (in currency)')
ax.legend()

# Format date on x-axis for better readability
plt.xticks(rotation=45, ha='right')

# Display the plot in Streamlit
st.pyplot(fig)

# Streamlit app setup
st.title('2. Distribution of Price and Freight Value')

# Create two subplots: one for Price distribution, one for Freight Value distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot 1: Price Distribution
ax1.hist(data['price'], bins=50, color='blue', alpha=0.7)
ax1.set_title('Price Distribution')
ax1.set_xlabel('Price (in currency)')
ax1.set_ylabel('Frequency')

# Plot 2: Freight Value Distribution
ax2.hist(data['freight_value'], bins=50, color='orange', alpha=0.7)
ax2.set_title('Freight Value Distribution')
ax2.set_xlabel('Freight Value (in currency)')
ax2.set_ylabel('Frequency')

# Adjust layout for better visualization
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Streamlit app setup
st.title('3. Price vs Freight Value by Product Category')

# Scatter plot: Price vs Freight Value with color-coded product categories
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter plot: each product category will be plotted with a different color
categories = data['product_category_name'].unique()
for category in categories:
    category_data = data[data['product_category_name'] == category]
    ax.scatter(category_data['price'], category_data['freight_value'], label=category, alpha=0.6)

ax.set_title('Price vs Freight Value by Product Category')
ax.set_xlabel('Price (in currency)')
ax.set_ylabel('Freight Value (in currency)')
ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

# Display the plot in Streamlit
st.pyplot(fig)

# Streamlit app setup
st.title('4. Price Distribution by Product Category')

# Filter the top 10 most common product categories to avoid clutter
top_categories = data['product_category_name'].value_counts().index[:10]
filtered_data = data[data['product_category_name'].isin(top_categories)]

# Box plot: Price distribution for each product category
fig, ax = plt.subplots(figsize=(10, 6))

# Create the boxplot
filtered_data.boxplot(column='price', by='product_category_name', ax=ax, grid=False, vert=False)

ax.set_title('Price Distribution by Product Category')
ax.set_xlabel('Price (in currency)')
ax.set_ylabel('Product Category')
plt.suptitle('')  # Remove the automatic boxplot title

# Display the plot in Streamlit
st.pyplot(fig)

# Streamlit app setup
st.title('5. Number of Orders per Customer')

# Assuming there is a 'customer_id' column in the dataset
# Count the number of orders per customer
order_count_per_customer = data['order_id'].groupby(data['order_id']).count()

# Filter the top 10 customers with the most orders
top_customers = order_count_per_customer.sort_values(ascending=False).head(10)

# Bar plot: Number of orders per top 10 customers
fig, ax = plt.subplots(figsize=(10, 6))
top_customers.plot(kind='bar', ax=ax, color='purple')

ax.set_title('Top 10 Customers by Number of Orders')
ax.set_xlabel('Customer ID')
ax.set_ylabel('Number of Orders')

# Display the plot in Streamlit
st.pyplot(fig)

# Streamlit app setup
st.title('6. Proportion of Total Spending by Top 5 Customers')

# Assuming there is a 'customer_id' column in the dataset and 'price' as the order value
# Calculate total spending by each customer
total_spending_per_customer = data.groupby('order_id')['price'].sum()

# Sort customers by total spending and get the top 5
top_5_customers = total_spending_per_customer.sort_values(ascending=False).head(5)

# Pie chart: Proportion of total spending by top 5 customers
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(top_5_customers, labels=top_5_customers.index, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen', 'lightcoral', 'gold', 'lightpink'])
ax.set_title('Proportion of Total Spending by Top 5 Customers')

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Display the plot in Streamlit
st.pyplot(fig)

 Streamlit app setup
st.title('7. Number of Orders by Shipping Location')

# Assuming there is a 'shipping_state' or 'shipping_city' column in the dataset
# Group by shipping location (city or state) and count the number of orders
location_order_count = data.groupby('shipping_city')['order_id'].count()

# Sort by the number of orders and display the top 10 locations
top_locations = location_order_count.sort_values(ascending=False).head(10)

# Bar plot: Number of orders by top 10 shipping locations
fig, ax = plt.subplots(figsize=(10, 6))
top_locations.plot(kind='bar', ax=ax, color='lightblue')

ax.set_title('Top 10 Shipping Locations by Number of Orders')
ax.set_xlabel('Shipping Location (City)')
ax.set_ylabel('Number of Orders')

# Display the plot in Streamlit
st.pyplot(fig)
