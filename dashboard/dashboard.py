import streamlit as st
import pandas as pd
import calendar

data = pd.read_csv('main_data.csv')

# Title
st.title('Bike Sharing Dashboard')

# Sidebar
st.sidebar.header('Filter Data')
season_filter = st.sidebar.selectbox('Select Season', data['season'].unique())
holiday_filter = st.sidebar.checkbox('Filter by Holiday')

# Filter sesuai pilihan
filtered_df = data[(data['season'] == season_filter) & (data['holiday'] == holiday_filter)]

# Kita buat formatting hari untuk digunakan di 'Bar Chart' jumlah sewa sepeda berdasarkan hari
# Ubah nilai dari weekday (0 - 6) jadi nama hari
filtered_df['weekday'] = filtered_df['weekday'].apply(lambda x: calendar.day_name[x])

# Menyesuaikan format internasional (mulai: Minggu, akhir: Sabtu)
weekday_order = list(calendar.day_name)
weekday_order = weekday_order[6:] + weekday_order[:6]
filtered_df['weekday'] = pd.Categorical(filtered_df['weekday'], categories=weekday_order, ordered=True)
filtered_df = filtered_df.sort_values('weekday')

# Menampilkan teks sesuai filter
st.write(f"Showing data for Season {season_filter} {'with' if holiday_filter else 'without'} holiday:")
st.write(filtered_df)

# Plotting
st.header('Data Visualization')

# Plot bar untuk penyewa casual dan tetap/berlangganan
st.subheader('Bar chart for Casual and Registered Users')
st.bar_chart(filtered_df[['casual', 'registered']])

# Line chart funtuk mengetahui jumlah sepeda yang disewa berdasarkan filter
st.subheader(f'Line chart for Bike Counts according to season {season_filter}')
st.line_chart(filtered_df['cnt'])

# Bar chart untuk menampilkan jumlah sepeda yang disewa sesuai dengan hari
st.subheader('Bar chart for Bike Counts based on Weekday')
weekday_counts = filtered_df.groupby('weekday')['cnt'].sum()
st.bar_chart(weekday_counts)

# Data Statistics
st.header('Data Statistics')
st.write(filtered_df.describe())
