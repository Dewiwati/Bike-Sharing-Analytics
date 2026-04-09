# 🚲 Bike Sharing Analytics Dashboard

Dashboard interaktif untuk menganalisis pola peminjaman sepeda dari sistem Capital Bikeshare, Washington D.C. (2011–2012).

## 📁 Struktur Direktori

```
submission
├── dashboard/
│   ├── main_data.csv       # Data harian yang sudah diproses
│   ├── hour_data.csv       # Data per jam yang sudah diproses
│   └── dashboard.py        # Aplikasi Streamlit
├── data/
│   ├── day.csv             # Dataset harian mentah
│   └── hour.csv            # Dataset per jam mentah
├── Proyek_Analisis_Data.ipynb          # Jupyter Notebook analisis lengkap
├── README.md               # File ini
├── requirements.txt        # Daftar library
└── url.txt                 # URL dashboard (jika sudah di-deploy)
```

## Pertanyaan Bisnis

1. **Bagaimana pengaruh musim dan kondisi cuaca terhadap jumlah peminjaman sepeda?**
2. **Bagaimana pola peminjaman berdasarkan jam, dan apakah ada perbedaan antara hari kerja dan hari libur?**

## Cara Menjalankan Dashboard

### Prasyarat

Pastikan Python 3.8+ sudah terinstal.

### Langkah 1: Clone / Ekstrak Folder

```bash
cd submission
```

### Langkah 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Langkah 3: Jalankan Dashboard

```bash
streamlit run dashboard/dashboard.py
```

### Langkah 4: Buka Browser

Dashboard akan otomatis terbuka di `http://localhost:8501`

## Fitur Dashboard

- **Filter** tanggal dan musim interaktif di sidebar
- **KPI Metrics** — total peminjaman, rata-rata harian, jumlah hari, dan puncak peminjaman
- **Visualisasi Musim & Cuaca** — pengaruh faktor lingkungan terhadap rata-rata peminjaman harian
- **Pola Jam** — perbandingan pola commuter (hari kerja) vs rekreasi (hari libur/weekend)
- **Demand Clustering** — pengelompokan hari berdasarkan intensitas permintaan (Low / Medium / High)

## Library yang Digunakan

Lihat `requirements.txt` untuk daftar lengkap.

## Sumber Data

- **Dataset:** Bike Sharing Dataset
- **Sumber:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset)
- **Referensi:** Fanaee-T, Hadi, and Gama, Joao (2013). _Event labeling combining ensemble detectors and background knowledge_. Progress in Artificial Intelligence.
