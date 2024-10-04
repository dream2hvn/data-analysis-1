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

# Load the data
data = pd.read_csv('all_data.csv')

# Convert 'shipping_limit_date' to datetime format for easier plotting
data['shipping_limit_date'] = pd.to_datetime(data['shipping_limit_date'], errors='coerce')

# Remove rows with NaT (not a valid datetime)
data = data.dropna(subset=['shipping_limit_date'])

# Sort data by date to ensure proper plotting
data = data.sort_values('shipping_limit_date')

# Streamlit app setup
st.title('Price and Freight Value Over Time')

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
st.title('Distribution of Price and Freight Value')

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
st.title('Price vs Freight Value by Product Category')

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
