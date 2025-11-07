import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

url_day = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/refs/heads/main/day.csv"
url_hour = "https://raw.githubusercontent.com/ibnuaditya-tech/Data-Analisis1/main/hour.csv"

day_df = pd.read_csv(url_day)
hour_df = pd.read_csv(url_hour)

day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

day_df['month'] = day_df['dteday'].dt.month
hour_df['month'] = hour_df['dteday'].dt.month

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].map(season_map)
hour_df['season'] = hour_df['season'].map(season_map)

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Dashboard Analisis Data Penyewaan Sepeda")
st.sidebar.header("Filter Data")

data_option = st.sidebar.radio("Pilih dataset:", ["Harian (day)", "Per Jam (hour)"])

seasons = ['All'] + sorted(day_df['season'].dropna().unique().tolist())
selected_season = st.sidebar.selectbox("Pilih Musim:", seasons)

if data_option == "Harian (day)":
    months = ['All'] + sorted(day_df['month'].unique().tolist())
    selected_month = st.sidebar.selectbox("Pilih Bulan:", months)

if data_option == "Per Jam (hour)":
    hours = ['All'] + sorted(hour_df['hr'].unique().tolist())
    selected_hour = st.sidebar.selectbox("Pilih Jam:", hours)

if data_option == "Harian (day)":
    filtered_df = day_df.copy()
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['season'] == selected_season]
    if selected_month != 'All':
        filtered_df = filtered_df[filtered_df['month'] == selected_month]
else:
    filtered_df = hour_df.copy()
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['season'] == selected_season]
    if selected_hour != 'All':
        filtered_df = filtered_df[filtered_df['hr'] == selected_hour]

st.subheader("Visualisasi Data")

col1, col2 = st.columns(2)

with col1:
    season_avg = filtered_df.groupby('season')['cnt'].mean().reset_index()
    st.markdown("**Rata-rata Penyewaan per musim**")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=season_avg, x='season', y='cnt', palette='viridis', ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

with col2:
    if data_option == "Harian (day)":
        month_avg = filtered_df.groupby('month')['cnt'].mean().reset_index()
        st.markdown("**Rata-rata penyewaan per bulan**")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.barplot(data=month_avg, x='month', y='cnt', palette='coolwarm', ax=ax2)
        ax2.set_xlabel("Bulan")
        ax2.set_ylabel("Rata-rata penyewaan")
        st.pyplot(fig2)
    else:
        hour_avg = filtered_df.groupby('hr')['cnt'].mean().reset_index()
        st.markdown("**Rata-rata penyewaan per jam**")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=hour_avg, x='hr', y='cnt', marker='o', ax=ax3)
        ax3.set_xlabel("Jam (0–23)")
        ax3.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig3)





