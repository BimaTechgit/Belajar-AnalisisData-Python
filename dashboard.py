import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
day_df = pd.read_csv("d:\day.csv")
hour_df = pd.read_csv("d:\hour.csv")

# Streamlit title
st.title("🚴 Dashboard Pertanyaan 1: Analisis Penyewaan Sepeda Berdasarkan Cuaca")

# 1️⃣ Menampilkan statistik umum
st.header("📊 Statistik Data")
st.write(day_df.describe())

# 2️⃣ Korelasi faktor cuaca terhadap penyewaan
st.header("🌤️ Korelasi Faktor Cuaca dengan Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(day_df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr(), annot=True, cmap="coolwarm", ax=ax)
plt.title("Korelasi antara Faktor Cuaca dan Jumlah Penyewaan Sepeda")
st.pyplot(fig)

st.markdown("""
✅ **Suhu memiliki korelasi positif dengan penyewaan sepeda**  
✅ **Kelembaban dan kecepatan angin cenderung memiliki korelasi negatif**  
""")

# 3️⃣ Rata-rata penyewaan berdasarkan kondisi cuaca
st.header("🌦️ Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
cuaca_avg = day_df.groupby("weathersit")["cnt"].mean()
fig, ax = plt.subplots()
colors = ["skyblue", "cadetblue", "grey"]
weather_labels = ["Cerah", "Berawan", "Hujan"]
ax.bar(weather_labels, cuaca_avg.values, color=colors)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
st.pyplot(fig)

st.markdown("""
✅ **Cuaca cerah memiliki jumlah penyewaan tertinggi**  
✅ **Saat hujan, jumlah penyewaan turun drastis**  
""")

# 4️⃣ Penyewaan sepeda berdasarkan musim
st.header("🍂 Penyewaan Sepeda Berdasarkan Musim")
season_total = day_df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots()
colors = ["skyblue","pink", "khaki", "orange"]
season_labels = ["winter", "spring", "summer", "fall"]
ax.bar(season_labels, season_total.values, color=colors)
ax.set_ylabel("Total Penyewaan Sepeda")
plt.title("Total Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

figur = plt.figure(figsize=(5,6))
# Menghitung total penyewaan untuk setiap musim
season_total = day_df.groupby("season")["cnt"].sum()

# Menggunakan data total penyewaan per musim untuk pie chart
plt.pie(season_total,
        labels=["Winter", "Spring", "Summer", "Fall"],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette(["skyblue", "pink", "khaki", "orange"], n_colors=4))

plt.xlabel("Musim")
plt.title("Persentase Penyewaan Sepeda berdasarkan Musim")
st.pyplot(figur)

st.markdown("""
✅ **Musim panas atau summer memiliki jumlah penyewaan tertinggi**  
✅ **Musim dingin atau winter memiliki jumlah penyewaan terendah**  
""")

# 5️⃣ Analisis dampak suhu dan kelembaban
st.header("🌡️ Dampak Suhu dan Kelembaban terhadap Penyewaan Sepeda")

# Kuartil suhu dan kelembaban
temp_q3 = day_df["temp"].quantile(0.75)
hum_q3 = day_df["hum"].quantile(0.75)

high_temp_rentals = day_df[day_df["temp"] >= temp_q3]["cnt"].mean()
low_temp_rentals = day_df[day_df["temp"] < temp_q3]["cnt"].mean()

high_hum_rentals = day_df[day_df["hum"] >= hum_q3]["cnt"].mean()
low_hum_rentals = day_df[day_df["hum"] < hum_q3]["cnt"].mean()

st.markdown(f"""
✅ **Rata-rata penyewaan pada suhu tinggi:** `{high_temp_rentals:.2f}` sepeda  
✅ **Rata-rata penyewaan pada suhu rendah:** `{low_temp_rentals:.2f}` sepeda  
✅ **Rata-rata penyewaan pada kelembaban tinggi:** `{high_hum_rentals:.2f}` sepeda  
✅ **Rata-rata penyewaan pada kelembaban rendah:** `{low_hum_rentals:.2f}` sepeda  
""")

# **Selesai**
st.markdown("### ✅ **Kesimpulan Akhir**")
st.markdown("""
- **Cuaca cerah dan suhu tinggi meningkatkan jumlah penyewaan sepeda**  
- **Musim gugur memiliki tingkat penyewaan tertinggi**  
- **Cuaca hujan dan kelembaban tinggi menurunkan jumlah penyewaan**  
""")

# =======================
# 🔍 ANALISIS DATA
# =======================
def analyze_peak_hours(data):
    busy_hour = data.groupby("hr")["cnt"].mean().idxmax()
    quiet_hour = data.groupby("hr")["cnt"].mean().idxmin()

    busy_hour_workday = data[data["workingday"] == 1].groupby("hr")["cnt"].mean().idxmax()
    busy_hour_weekend = data[data["workingday"] == 0].groupby("hr")["cnt"].mean().idxmax()

    return busy_hour, quiet_hour, busy_hour_workday, busy_hour_weekend

busy_hour, quiet_hour, busy_hour_workday, busy_hour_weekend = analyze_peak_hours(hour_df)

st.title("📊 Dashboard Pertanyaan 2: Waktu Paling Ramai dan Sepi untuk Penyewaan Sepeda 🚴")


# 📌 **Statistik Umum**
st.subheader("📌 Statistik Umum")
col1, col2 = st.columns(2)

with col1:
    st.metric("Jam Paling Ramai", f"{busy_hour}:00")
    st.metric("Jam Paling Sepi", f"{quiet_hour}:00")

with col2:
    st.metric("Puncak Hari Kerja", f"{busy_hour_workday}:00")
    st.metric("Puncak Akhir Pekan", f"{busy_hour_weekend}:00")

# 📊 **Distribusi Penyewaan Sepeda per Jam**
st.subheader("📊 Distribusi Penyewaan Sepeda per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hour_df["hr"], y=hour_df["cnt"], ci=None, marker="o", color="b")
plt.xticks(np.arange(0, 24, 1))
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Distribusi Penyewaan Sepeda per Jam")
plt.grid()
st.pyplot(fig)

# 🔄 **Pola Hari Kerja vs Akhir Pekan**
st.subheader("📊 Pola Penyewaan: Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hour_df, x="hr", y="cnt", hue="workingday", ci=None, marker="o")
plt.xticks(np.arange(0, 24, 1))
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Jumlah Penyewaan Sepeda")
plt.title("Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
plt.legend(["Akhir Pekan", "Hari Kerja"])
plt.grid()
st.pyplot(fig)

# ✅ **Kesimpulan Akhir**
st.subheader("✅ Kesimpulan")
st.write("""
- **Jam paling ramai** untuk penyewaan sepeda adalah **jam 17:00** (pulang kerja).
- **Jam paling sepi** adalah **jam 03:00** (dini hari, sedikit aktivitas).
- **Hari kerja** memiliki dua puncak utama: **08:00 (berangkat kerja)** & **17:00 (pulang kerja)**.
- **Akhir pekan** lebih fleksibel, dengan puncak penyewaan sekitar **14:00**.
""")

# Sidebar untuk memilih tampilan
st.sidebar.title("🚴 Dashboard Bike Sharing")
option = st.sidebar.selectbox("Pilih Analisis:", [
    "Jumlah Pengguna Terdaftar vs Tidak Terdaftar",
    "Tren Pengguna Sepeda"
])

# 📌 1. Jumlah Pengguna Terdaftar vs Tidak Terdaftar
if option == "Jumlah Pengguna Terdaftar vs Tidak Terdaftar":
    st.title("🔍 Dashboard Pertanyaan 3: Perbandingan Pengguna Terdaftar vs Tidak Terdaftar")
    
    st.header("📊 Perbandingan Pengguna Terdaftar dan Tidak Terdaftar")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(['Registered', 'Casual'], [day_df['registered'].sum(), day_df['casual'].sum()], color=['blue', 'orange'])
    ax.set_ylabel("Total Penyewaan")
    ax.set_title("Total Penyewaan Sepeda Berdasarkan Jenis Pengguna")
    st.pyplot(fig)

    total_registered = hour_df['registered'].sum()
    total_casual = hour_df['casual'].sum()
    
    st.write("**Total Pengguna Terdaftar:**", total_registered)
    st.write("**Total Pengguna Tidak Terdaftar:**", total_casual)
    
    # Pie chart
    fig, ax = plt.subplots()
    ax.pie([total_registered, total_casual], labels=["Terdaftar", "Tidak Terdaftar"], autopct='%1.1f%%', colors=["#1f77b4", "#ff7f0e"])
    st.pyplot(fig)

    st.subheader("✅ Kesimpulan")
    st.write("""
    - **Pengguna terdaftar menyewa lebih banyak sepeda dibanding tidak terdaftar.
    - **Hari kerja didominasi oleh pengguna terdaftar.
    - **Akhir pekan lebih banyak digunakan oleh pengguna tidak terdaftar.
    """)

# 📌 2. Tren Pengguna Sepeda Sepanjang Waktu
elif option == "Tren Pengguna Sepeda":
    st.title("📈 Tren Penyewaan Sepeda")
    df_daily = hour_df.groupby('dteday').agg({'registered': 'sum', 'casual': 'sum'}).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='dteday', y='registered', data=df_daily, label='Terdaftar', color='blue')
    sns.lineplot(x='dteday', y='casual', data=df_daily, label='Tidak Terdaftar', color='orange')
    plt.xticks(rotation=45)
    plt.title("Tren Pengguna Sepeda per Hari")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(fig)