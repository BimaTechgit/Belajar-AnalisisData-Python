# Belajar-AnalisisData-Python

# 🚴 Bike Sharing Analysis

## 📌 Project Overview
Analisis data penyewaan sepeda untuk memahami faktor-faktor yang mempengaruhi penggunaan sepeda berdasarkan dataset **Bike Sharing Dataset**. Analisis ini mencakup:
1. **Pengaruh Faktor Cuaca terhadap Jumlah Penyewaan Sepeda**
2. **Waktu Paling Ramai dan Sepi untuk Penyewaan Sepeda**
3. **Perbandingan Penggunaan Sepeda antara Pengguna Terdaftar dan Tidak Terdaftar**
4. **RFM Analysis untuk Segmentasi Pengguna**


## 🛠 Setup Environment (Anaconda)
Sebelum menjalankan proyek ini, pastikan **Anaconda** telah terinstal di sistem Anda.

### **1. Buat dan Aktifkan Virtual Environment**
```sh
conda create -n bike-sharing-env python=3.12 -y
conda activate bike-sharing-env
pip install -r requirements.txt
```

## 📂 Dataset
Dataset tersedia dalam folder bernama `data`, terdapat dua file utama yang digunakan:
- `day.csv`: Data harian penyewaan sepeda
- `hour.csv`: Data penyewaan sepeda per jam

Pastikan file dataset diletakkan di dalam folder proyek sebelum menjalankan analisis.

## 🚀 Cara Menjalankan Analisis via anaconda
Buka **Jupyter Notebook** dan jalankan skrip analisis dengan perintah:
```sh
jupyter notebook
```

Lalu buka file notebook yang telah dibuat dan jalankan setiap sel kode sambil upload dataset pada folder `data`.

## 🚀 Cara Menjalankan Analisis via google colab
jika ingin lebih cepat dan tidak ingin install anaconda cukup bukan google colab upload file `notebook.ipynb` pada google colab dan upload file dari folder `data` serta jalankan setiap sel pada blok kode

jika ingin menjalankan skrip Python langsung di terminal:
```sh
streamlit run bike_sharing_analysis.py
```

## 📊 Visualisasi Data
Analisis ini menggunakan **Matplotlib dan Seaborn** untuk visualisasi:
- Grafik tren penyewaan sepeda berdasarkan cuaca
- Grafik jumlah penyewaan per jam
- Grafik perbandingan pengguna terdaftar dan tidak terdaftar
- Analisis RFM untuk segmentasi pengguna

## 📝 To-Do List / Pengembangan Selanjutnya
- Menambahkan **Clustering (K-Means) berdasarkan hasil RFM** untuk segmentasi lebih akurat
- Menggunakan **Dash atau Streamlit** untuk membuat dashboard interaktif

## 📌 License
Project ini bersifat open-source, silakan gunakan dan kembangkan sesuai kebutuhan Anda.

---
🚴 **Happy Analyzing!**

 
