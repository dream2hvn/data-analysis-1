# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HrWbeuarj6T4gAc6b15lu6woa7GsLevn
"""
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

# Fungsi untuk menghitung RFM
def calculate_rfm(orders, customers, order_items):
    # Mengonversi kolom order_purchase_timestamp menjadi datetime
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
    orders.dropna(subset=['order_purchase_timestamp'], inplace=True)

    current_date = orders['order_purchase_timestamp'].max()

    # Gabungkan orders dengan customers berdasarkan customer_id untuk mendapatkan informasi pelanggan
    orders_customers = pd.merge(orders[['order_id', 'customer_id', 'order_purchase_timestamp']],
                                customers,
                                on='customer_id',
                                how='inner')

    # Menghitung recency (hari sejak pembelian terakhir)
    recency = orders_customers.groupby('customer_unique_id').agg(
        last_purchase=('order_purchase_timestamp', 'max')
    ).reset_index()

    recency['recency'] = (current_date - recency['last_purchase']).dt.days

    # Menghitung frequency (jumlah order per pelanggan)
    frequency = orders_customers.groupby('customer_unique_id').agg(
        frequency=('order_id', 'count')
    ).reset_index()

    # Menghitung monetary (total pembelanjaan per pelanggan)
    monetary = pd.merge(orders_customers[['order_id', 'customer_unique_id']],
                        order_items[['order_id', 'price']],
                        on='order_id',
                        how='inner')

    monetary = monetary.groupby('customer_unique_id').agg(
        total_spent=('price', 'sum')
    ).reset_index()

    # Menggabungkan recency, frequency, dan monetary menjadi satu dataframe RFM
    rfm = pd.merge(recency[['customer_unique_id', 'recency']],
                   frequency[['customer_unique_id', 'frequency']],
                   on='customer_unique_id')

    rfm = pd.merge(rfm,
                   monetary[['customer_unique_id', 'total_spent']],
                   on='customer_unique_id')

    return rfm

# Menghitung RFM
rfm = calculate_rfm(orders, customers, order_items)

# Menampilkan judul aplikasi
st.title('Visualisasi RFM Dataset')

# Pilihan untuk tipe visualisasi
visualization_type = st.selectbox(
    'Pilih Visualisasi',
    ('Histogram', 'Scatter Plot', 'Heatmap Korelasi')
)

# Menampilkan visualisasi berdasarkan pilihan pengguna
if visualization_type == 'Histogram':
    # Pilih variabel untuk ditampilkan di histogram
    variable = st.selectbox('Pilih variabel untuk histogram', ('recency', 'frequency', 'total_spent'))

    # Membuat histogram
    st.subheader(f'Histogram dari {variable}')
    fig, ax = plt.subplots()
    sns.histplot(rfm[variable], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Scatter Plot':
    # Pilih variabel untuk scatter plot
    x_axis = st.selectbox('Pilih variabel X', ('recency', 'frequency', 'total_spent'))
    y_axis = st.selectbox('Pilih variabel Y', ('recency', 'frequency', 'total_spent'))

    # Membuat scatter plot
    st.subheader(f'Scatter Plot antara {x_axis} dan {y_axis}')
    fig, ax = plt.subplots()
    sns.scatterplot(x=rfm[x_axis], y=rfm[y_axis], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Heatmap Korelasi':
    # Membuat heatmap korelasi
    st.subheader('Heatmap Korelasi antara Recency, Frequency, dan Monetary')
    corr = rfm[['recency', 'frequency', 'total_spent']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

# Fungsi untuk menghitung RFM
def calculate_rfm(orders, customers, order_items):
    # Mengonversi kolom order_purchase_timestamp menjadi datetime
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
    orders.dropna(subset=['order_purchase_timestamp'], inplace=True)

    current_date = orders['order_purchase_timestamp'].max()

    # Gabungkan orders dengan customers berdasarkan customer_id untuk mendapatkan informasi pelanggan
    orders_customers = pd.merge(orders[['order_id', 'customer_id', 'order_purchase_timestamp']],
                                customers,
                                on='customer_id',
                                how='inner')

    # Menghitung recency (hari sejak pembelian terakhir)
    recency = orders_customers.groupby('customer_unique_id').agg(
        last_purchase=('order_purchase_timestamp', 'max')
    ).reset_index()

    recency['recency'] = (current_date - recency['last_purchase']).dt.days

    # Menghitung frequency (jumlah order per pelanggan)
    frequency = orders_customers.groupby('customer_unique_id').agg(
        frequency=('order_id', 'count')
    ).reset_index()

    # Menghitung monetary (total pembelanjaan per pelanggan)
    monetary = pd.merge(orders_customers[['order_id', 'customer_unique_id']],
                        order_items[['order_id', 'price']],
                        on='order_id',
                        how='inner')

    monetary = monetary.groupby('customer_unique_id').agg(
        total_spent=('price', 'sum')
    ).reset_index()

    # Menggabungkan recency, frequency, dan monetary menjadi satu dataframe RFM
    rfm = pd.merge(recency[['customer_unique_id', 'recency']],
                   frequency[['customer_unique_id', 'frequency']],
                   on='customer_unique_id')

    rfm = pd.merge(rfm,
                   monetary[['customer_unique_id', 'total_spent']],
                   on='customer_unique_id')

    return rfm

# Menghitung RFM
rfm = calculate_rfm(orders, customers, order_items)

# Menampilkan judul aplikasi
st.title('Visualisasi RFM Dataset')

# Pilihan untuk tipe visualisasi
visualization_type = st.selectbox(
    'Pilih Visualisasi',
    ('Histogram', 'Scatter Plot', 'Heatmap Korelasi', 'Boxplot', 'Pairplot', 'Bar Plot')
)

# Menampilkan visualisasi berdasarkan pilihan pengguna
if visualization_type == 'Histogram':
    # Pilih variabel untuk ditampilkan di histogram
    variable = st.selectbox('Pilih variabel untuk histogram', ('recency', 'frequency', 'total_spent'))

    # Membuat histogram
    st.subheader(f'Histogram dari {variable}')
    fig, ax = plt.subplots()
    sns.histplot(rfm[variable], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Scatter Plot':
    # Pilih variabel untuk scatter plot
    x_axis = st.selectbox('Pilih variabel X', ('recency', 'frequency', 'total_spent'))
    y_axis = st.selectbox('Pilih variabel Y', ('recency', 'frequency', 'total_spent'))

    # Membuat scatter plot
    st.subheader(f'Scatter Plot antara {x_axis} dan {y_axis}')
    fig, ax = plt.subplots()
    sns.scatterplot(x=rfm[x_axis], y=rfm[y_axis], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Heatmap Korelasi':
    # Membuat heatmap korelasi
    st.subheader('Heatmap Korelasi antara Recency, Frequency, dan Monetary')
    corr = rfm[['recency', 'frequency', 'total_spent']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Boxplot':
    # Pilih variabel untuk ditampilkan di boxplot
    variable = st.selectbox('Pilih variabel untuk boxplot', ('recency', 'frequency', 'total_spent'))

    # Membuat boxplot
    st.subheader(f'Boxplot dari {variable}')
    fig, ax = plt.subplots()
    sns.boxplot(y=rfm[variable], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Pairplot':
    # Membuat pairplot untuk semua variabel RFM
    st.subheader('Pairplot dari Recency, Frequency, dan Monetary')
    fig = sns.pairplot(rfm[['recency', 'frequency', 'total_spent']])
    st.pyplot(fig)

elif visualization_type == 'Bar Plot':
    # Membuat bar plot rata-rata dari Recency, Frequency, dan Monetary
    st.subheader('Bar Plot dari Rata-rata Recency, Frequency, dan Monetary')
    averages = rfm[['recency', 'frequency', 'total_spent']].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=averages.index, y=averages.values, ax=ax)
    ax.set_ylabel('Rata-rata')
    st.pyplot(fig)

# Fungsi untuk menghitung RFM
def calculate_rfm(orders, customers, order_items):
    # Mengonversi kolom order_purchase_timestamp menjadi datetime
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
    orders.dropna(subset=['order_purchase_timestamp'], inplace=True)

    current_date = orders['order_purchase_timestamp'].max()

    # Gabungkan orders dengan customers berdasarkan customer_id untuk mendapatkan informasi pelanggan
    orders_customers = pd.merge(orders[['order_id', 'customer_id', 'order_purchase_timestamp']],
                                customers,
                                on='customer_id',
                                how='inner')

    # Menghitung recency (hari sejak pembelian terakhir)
    recency = orders_customers.groupby('customer_unique_id').agg(
        last_purchase=('order_purchase_timestamp', 'max')
    ).reset_index()

    recency['recency'] = (current_date - recency['last_purchase']).dt.days

    # Menghitung frequency (jumlah order per pelanggan)
    frequency = orders_customers.groupby('customer_unique_id').agg(
        frequency=('order_id', 'count')
    ).reset_index()

    # Menghitung monetary (total pembelanjaan per pelanggan)
    monetary = pd.merge(orders_customers[['order_id', 'customer_unique_id']],
                        order_items[['order_id', 'price']],
                        on='order_id',
                        how='inner')

    monetary = monetary.groupby('customer_unique_id').agg(
        total_spent=('price', 'sum')
    ).reset_index()

    # Menggabungkan recency, frequency, dan monetary menjadi satu dataframe RFM
    rfm = pd.merge(recency[['customer_unique_id', 'recency']],
                   frequency[['customer_unique_id', 'frequency']],
                   on='customer_unique_id')

    rfm = pd.merge(rfm,
                   monetary[['customer_unique_id', 'total_spent']],
                   on='customer_unique_id')

    return rfm

# Menghitung RFM
rfm = calculate_rfm(orders, customers, order_items)

# Menampilkan judul aplikasi
st.title('Visualisasi RFM Dataset')

# Pilihan untuk tipe visualisasi
visualization_type = st.selectbox(
    'Pilih Visualisasi',
    ('Histogram', 'Scatter Plot', 'Heatmap Korelasi', 'Boxplot', 'Pairplot', 'Bar Plot', 'Violin Plot', 'Line Plot', 'Count Plot')
)

# Menampilkan visualisasi berdasarkan pilihan pengguna
if visualization_type == 'Histogram':
    # Pilih variabel untuk ditampilkan di histogram
    variable = st.selectbox('Pilih variabel untuk histogram', ('recency', 'frequency', 'total_spent'))

    # Membuat histogram
    st.subheader(f'Histogram dari {variable}')
    fig, ax = plt.subplots()
    sns.histplot(rfm[variable], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Scatter Plot':
    # Pilih variabel untuk scatter plot
    x_axis = st.selectbox('Pilih variabel X', ('recency', 'frequency', 'total_spent'))
    y_axis = st.selectbox('Pilih variabel Y', ('recency', 'frequency', 'total_spent'))

    # Membuat scatter plot
    st.subheader(f'Scatter Plot antara {x_axis} dan {y_axis}')
    fig, ax = plt.subplots()
    sns.scatterplot(x=rfm[x_axis], y=rfm[y_axis], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Heatmap Korelasi':
    # Membuat heatmap korelasi
    st.subheader('Heatmap Korelasi antara Recency, Frequency, dan Monetary')
    corr = rfm[['recency', 'frequency', 'total_spent']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Boxplot':
    # Pilih variabel untuk ditampilkan di boxplot
    variable = st.selectbox('Pilih variabel untuk boxplot', ('recency', 'frequency', 'total_spent'))

    # Membuat boxplot
    st.subheader(f'Boxplot dari {variable}')
    fig, ax = plt.subplots()
    sns.boxplot(y=rfm[variable], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Pairplot':
    # Membuat pairplot untuk semua variabel RFM
    st.subheader('Pairplot dari Recency, Frequency, dan Monetary')
    fig = sns.pairplot(rfm[['recency', 'frequency', 'total_spent']])
    st.pyplot(fig)

elif visualization_type == 'Bar Plot':
    # Membuat bar plot rata-rata dari Recency, Frequency, dan Monetary
    st.subheader('Bar Plot dari Rata-rata Recency, Frequency, dan Monetary')
    averages = rfm[['recency', 'frequency', 'total_spent']].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=averages.index, y=averages.values, ax=ax)
    ax.set_ylabel('Rata-rata')
    st.pyplot(fig)

elif visualization_type == 'Violin Plot':
    # Pilih variabel untuk violin plot
    variable = st.selectbox('Pilih variabel untuk violin plot', ('recency', 'frequency', 'total_spent'))

    # Membuat violin plot
    st.subheader(f'Violin Plot dari {variable}')
    fig, ax = plt.subplots()
    sns.violinplot(y=rfm[variable], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Line Plot':
    # Pilih variabel untuk line plot
    variable = st.selectbox('Pilih variabel untuk line plot', ('recency', 'frequency', 'total_spent'))

    # Membuat line plot
    st.subheader(f'Line Plot dari {variable}')
    fig, ax = plt.subplots()
    sns.lineplot(data=rfm[variable], ax=ax)
    st.pyplot(fig)

elif visualization_type == 'Count Plot':
    # Membuat count plot untuk frekuensi order
    st.subheader('Count Plot dari Frequency (Jumlah Order)')
    fig, ax = plt.subplots()
    sns.countplot(x=rfm['frequency'], ax=ax)
    st.pyplot(fig)
