import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/BimaTechgit/Belajar-AnalisisData-Python/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/anandashadrina/BikeSharingDataset-Dicoding/refs/heads/main/data/hour.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Judul dan identitas
st.markdown("""
 **Nama     : Bimasakti Faturrahman Soetedjo**  
 **Email    : riqjuniorbimasakti@gmail.com**  
 **Dicoding : BimaTech**  
""")

st.title("🚴 Dashboard Analisis Pertanyaan 1: Pengaruh Cuaca terhadap Penyewaan Sepeda")
st.markdown(f"""**fitur interaktif diberikan hanya kepada pertanyaan 1 karena pada pertanyaan ini yang paling banyak terjadi analisa penting**""")
# ======= Inisialisasi session_state untuk reset ========
if "reset" not in st.session_state:
    st.session_state["reset"] = False

# ======= Sidebar Filter & Reset ========
st.sidebar.header("🔍 Filter Data pertanyaan 1:")

# Inisialisasi default
default_date = [day_df['dteday'].min(), day_df['dteday'].max()]
default_season = [1, 2, 3, 4]
default_weather = [1, 2, 3]

# Reset tombol
if "reset_triggered" not in st.session_state:
    st.session_state["reset_triggered"] = False

if st.sidebar.button("🔄 Reset Filter"):
    st.session_state["reset_triggered"] = True
    st.session_state["start_date"] = pd.to_datetime(day_df['dteday'].min())
    st.session_state["end_date"] = pd.to_datetime(day_df['dteday'].max())
    st.session_state["season_filter"] = default_season.copy()
    st.session_state["weather_filter"] = default_weather.copy()

# Atur default filter jika belum ada di session_state
if "date_range" not in st.session_state:
    st.session_state["date_range"] = default_date
if "season_filter" not in st.session_state:
    st.session_state["season_filter"] = default_season
if "weather_filter" not in st.session_state:
    st.session_state["weather_filter"] = default_weather

# Widget filter yang tetap muncul
start_date = st.sidebar.date_input(
    "Tanggal Mulai",
    value=st.session_state.get("start_date", pd.to_datetime(day_df['dteday'].min()))
)
end_date = st.sidebar.date_input(
    "Tanggal Akhir",
    value=st.session_state.get("end_date", pd.to_datetime(day_df['dteday'].max()))
)

st.session_state.setdefault("season_filter", default_season)
st.session_state.setdefault("weather_filter", default_weather)

st.sidebar.subheader("🌸 Filter Musim & Cuaca")
st.sidebar.multiselect(
    "Pilih Musim (season):",
    options=[1, 2, 3, 4],
    default=st.session_state["season_filter"],
    key="season_filter"
)

st.sidebar.multiselect(
    "Pilih Kondisi Cuaca (weathersit):",
    options=[1, 2, 3],
    default=st.session_state["weather_filter"],
    key="weather_filter"
)

# Perbarui session_state jika user ubah filter
st.session_state["start_date"] = start_date
st.session_state["end_date"] = end_date


# Mapping label
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_map = {1: "Cerah", 2: "Berawan", 3: "Hujan"}

# Filter Data
filtered_day_df = day_df[
    (day_df['dteday'] >= pd.to_datetime(st.session_state["start_date"])) &
    (day_df['dteday'] <= pd.to_datetime(st.session_state["end_date"])) &
    (day_df['season'].isin(st.session_state["season_filter"])) &
    (day_df['weathersit'].isin(st.session_state["weather_filter"]))
]

# ======== Statistik Data =========
st.header("📊 Statistik Data (Setelah Filter)")
st.write(filtered_day_df.describe())

# ======== Korelasi Faktor Cuaca =========
st.header("🌤️ Korelasi Faktor Cuaca dengan Jumlah Penyewaan")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(filtered_day_df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr(), annot=True, cmap="coolwarm", ax=ax)
plt.title("Korelasi antara Faktor Cuaca dan Jumlah Penyewaan")
st.pyplot(fig)

# ======== Rata-rata Penyewaan Berdasarkan Cuaca ========
st.header("🌦️ Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
cuaca_avg = filtered_day_df.groupby("weathersit")["cnt"].mean()
fig, ax = plt.subplots()
colors = ["skyblue", "cadetblue", "grey"]
labels = [weather_map.get(i, f"Weathersit {i}") for i in cuaca_avg.index]
ax.bar(labels, cuaca_avg.values, color=colors[:len(labels)])
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
plt.title("Penyewaan Sepeda per Kondisi Cuaca")
st.pyplot(fig)

# ======== Rata-rata Penyewaan Berdasarkan Musim ========
st.header("🍂 Rata-rata Penyewaan Berdasarkan Musim")
season_avg = filtered_day_df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots()
season_labels = [season_map.get(i, f"Season {i}") for i in season_avg.index]
colors = ["skyblue", "pink", "khaki", "orange"]
ax.bar(season_labels, season_avg.values, color=colors[:len(season_labels)])
plt.title("Penyewaan Sepeda per Musim")
st.pyplot(fig)

# ======== Pie Chart Penyewaan per Musim ========
fig2 = plt.figure(figsize=(5,6))
season_total = filtered_day_df.groupby("season")["cnt"].sum()
plt.pie(season_total,
        labels=[season_map.get(i, f"Season {i}") for i in season_total.index],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(season_total)])
plt.title("Persentase Penyewaan Sepeda per Musim")
st.pyplot(fig2)

# ======== Dampak Suhu & Kelembaban ========
st.header("🌡️ Dampak Suhu dan Kelembaban terhadap Penyewaan Sepeda")
temp_q3 = filtered_day_df["temp"].quantile(0.75)
hum_q3 = filtered_day_df["hum"].quantile(0.75)

high_temp_rentals = filtered_day_df[filtered_day_df["temp"] >= temp_q3]["cnt"].mean()
low_temp_rentals = filtered_day_df[filtered_day_df["temp"] < temp_q3]["cnt"].mean()
high_hum_rentals = filtered_day_df[filtered_day_df["hum"] >= hum_q3]["cnt"].mean()
low_hum_rentals = filtered_day_df[filtered_day_df["hum"] < hum_q3]["cnt"].mean()

st.markdown(f"""
✅ **Rata-rata penyewaan saat suhu tinggi (≥ Q3):** `{high_temp_rentals:.2f}`  
✅ **Rata-rata penyewaan saat suhu rendah (< Q3):** `{low_temp_rentals:.2f}`  
✅ **Rata-rata penyewaan saat kelembaban tinggi (≥ Q3):** `{high_hum_rentals:.2f}`  
✅ **Rata-rata penyewaan saat kelembaban rendah (< Q3):** `{low_hum_rentals:.2f}`  
""")

# ======== Kesimpulan ========
st.header("✅ Kesimpulan Analisis")
st.markdown("""
- **Cuaca cerah dan suhu tinggi meningkatkan jumlah penyewaan sepeda**  
- **Musim summer (panas) memiliki penyewaan tertinggi, disusul fall (gugur)**  
- **Cuaca hujan dan kelembaban tinggi menurunkan jumlah penyewaan**  
- **Musim winter menunjukkan tingkat penyewaan terendah**  
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