
# Proyek Gudang Data SQL

Proyek ini adalah contoh pipeline ETL (Extract, Transform, Load) untuk membangun gudang data dari beberapa sumber data.

## Struktur Proyek

```
.
├── datasets
│   ├── source_crm
│   └── source_erp
├── scripts
│   ├── bronze
│   ├── gold
│   └── silver
├── tests
├── dashboard.py
├── etl_pipeline.py
├── generate_dummy_data.py
└── README.md
```

## Cara Menjalankan

### 1. Persyaratan

Pastikan Anda memiliki Python 3.8+ terinstal. Anda juga perlu menginstal beberapa pustaka Python.

```bash
pip install pandas sqlalchemy streamlit
```

### 2. Hasilkan Data Awal

Langkah pertama adalah menjalankan skrip untuk menghasilkan atau menyiapkan data mentah.

```bash
python generate_dummy_data.py
```

### 3. Bangun Gudang Data (ETL)

Setelah data mentah siap, jalankan pipeline ETL untuk memprosesnya dan memuatnya ke dalam gudang data dengan skema bintang.

```bash
python etl_pipeline.py
```

### 4. Jalankan Dashboard

Untuk memvisualisasikan data dan memastikan semuanya terhubung dengan benar, jalankan aplikasi dashboard Streamlit.

```bash
streamlit run dashboard.py
```

Buka browser Anda dan navigasikan ke alamat URL yang ditampilkan di terminal.
