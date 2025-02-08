import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("Dashboard/main_data.csv", delimiter=",")

def create_rent_by_hour(df):
    bike_rented_hour = main_df.groupby(by="hr")["cnt_hour"].sum().reset_index()
    bins = [0, 6, 12, 18, 23]
    labels = ['Dini Hari', 'Pagi', 'Siang', 'Malam']
    bike_rented_hour['Kategori Waktu'] = pd.cut(bike_rented_hour['hr'], bins=bins, labels=labels, include_lowest=True)

    return bike_rented_hour

def create_rent_by_weather(df):
    bike_rented_weather = main_df.groupby(by="weathersit_hour")["cnt_hour"].mean().reset_index()
    return bike_rented_weather

def create_rent_by_season(df):
    bike_rented_season = main_df.groupby('season_day')['cnt_day'].mean().reset_index()
    return bike_rented_season


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Dashboard/images.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

rent_by_hour = create_rent_by_hour(main_df)
rent_by_season = create_rent_by_season(main_df)
rent_by_weather = create_rent_by_weather(main_df)


st.header('Bike Rentals Dashboard :sparkles:')
 
col1, col2 = st.columns(2)
 
with col1:
    total_rented = main_df.cnt_hour.sum()
    st.metric("Total rented", value=total_rented)

st.subheader("Amount Of Bike Rented Per Hour")
plt.figure(figsize=(10, 5))
sns.barplot(x='hr', y='cnt_hour', hue='Kategori Waktu', data=rent_by_hour)
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.title('Clustering Penyewaan Sepeda Berdasarkan Waktu')
plt.legend(title='Kategori Waktu')
st.pyplot(plt.gcf())


st.subheader("Amount Of Bike Rented Based On Weather Situation")
plt.figure(figsize=(12, 6))
sns.barplot(data=rent_by_weather, x='weathersit_hour', y='cnt_hour')
plt.xlabel('Kondisi Cuaca (1=Clear, 2=Misty, 3=Light Snow/Rain, 4=Heavy Rain/Thunderstorm/Fog)')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')
st.pyplot(plt.gcf())


st.subheader("Amount Of Bike Rented By Seasons")
if rent_by_season.empty:
    st.warning("Tidak ada data dalam rentang tanggal yang dipilih.")
else:
    # Pastikan hanya musim yang ada dalam rentang yang dipilih
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    rent_by_season['season_label'] = rent_by_season['season_day'].map(season_mapping)

    plt.figure(figsize=(5, 3))
    plt.pie(
        rent_by_season['cnt_day'], 
        labels=rent_by_season['season_label'],  # Gunakan label dari data yang tersedia
        autopct='%1.1f%%', 
        colors=['lightblue', 'gold', 'orange', 'gray'], 
        wedgeprops={'width': 0.2}
    )
    plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
    st.pyplot(plt.gcf())





