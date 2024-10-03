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

# Judul Dashboard
st.title("Dashboard Analisis E-commerce")

# Fungsi untuk memuat dataset
@st.cache
def load_data():

# Peta interaktif dengan Folium
st.subheader("Peta Interaktif Pelanggan")
m = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)
marker_cluster = MarkerCluster().add_to(m)

for idx, row in geolocation.iterrows():
    folium.Marker(location=[row['geolocation_lat'], row['geolocation_lng']],
                  popup=row['geolocation_zip_code_prefix']).add_to(marker_cluster)
