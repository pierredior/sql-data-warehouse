import streamlit as st
import pandas as pd
import sqlite3
import os

DB_NAME = 'dwh.db'

# Mengatur konfigurasi halaman. Harus menjadi perintah pertama Streamlit.
st.set_page_config(
    page_title="Dashboard Penjualan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_data():
    """Memuat data dari database dan menggabungkan tabel."""
    if not os.path.exists(DB_NAME):
        return None, None, None
    
    conn = sqlite3.connect(DB_NAME)
    
    # Query utama untuk mengambil data penjualan yang sudah digabung dengan dimensi
    query = """
    SELECT
        fs.order_number,
        fs.order_date,
        fs.sales_amount,
        fs.quantity,
        dc.customer_id,
        dc.first_name,
        dc.last_name,
        dc.country,
        dc.marital_status,
        dc.gender,
        dp.product_id,
        dp.product_name,
        dp.category,
        dp.subcategory
    FROM gold_fact_sales fs
    LEFT JOIN gold_dim_customers dc ON fs.customer_key = dc.customer_key
    LEFT JOIN gold_dim_products dp ON fs.product_key = dp.product_key
    """
    try:
        df = pd.read_sql_query(query, conn)
        # Mengubah kolom tanggal menjadi datetime
        if not df.empty:
            df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Memuat dimensi secara terpisah untuk tampilan tabel
        df_customers = pd.read_sql_query("SELECT * FROM gold_dim_customers", conn)
        df_products = pd.read_sql_query("SELECT * FROM gold_dim_products", conn)
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        conn.close()
        return None, None, None

    conn.close()
    return df, df_customers, df_products

# --- Sidebar ---
with st.sidebar:
    st.title("📊 Dashboard Gudang Data")
    st.write("Proyek ini menampilkan pipeline ETL dan visualisasi data penjualan.")
    
    # Memuat data dan menangani kasus jika data tidak ada
    df, df_customers, df_products = load_data()

    if df is None or df.empty:
        st.error(f"Tidak ada data untuk ditampilkan. Pastikan database '{DB_NAME}' ada dan berisi data.")
        st.stop() # Menghentikan eksekusi jika data tidak ada

    st.header("Filter")
    # Filter berdasarkan negara
    all_countries = ["Semua"] + sorted(df['country'].dropna().unique().tolist())
    selected_country = st.selectbox("Pilih Negara", all_countries)

    # Filter berdasarkan kategori produk
    all_categories = ["Semua"] + sorted(df['category'].dropna().unique().tolist())
    selected_category = st.selectbox("Pilih Kategori Produk", all_categories)

# Filter data berdasarkan input sidebar
if selected_country != "Semua":
    df = df[df['country'] == selected_country]

if selected_category != "Semua":
    df = df[df['category'] == selected_category]

# --- Halaman Utama ---
st.title("📈 Analisis Penjualan")
st.markdown("---")

if df.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang Anda pilih.")
    st.stop()

# Metrik Utama
total_sales = df['sales_amount'].sum()
total_quantity = df['quantity'].sum()
total_orders = df['order_number'].nunique()
avg_sales_per_order = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penjualan", f"${total_sales:,.0f}")
col2.metric("Total Kuantitas", f"{total_quantity:,}")
col3.metric("Total Pesanan", f"{total_orders:,}")
col4.metric("Rata-rata Penjualan/Pesanan", f"${avg_sales_per_order:,.0f}")

st.markdown("---")

# Visualisasi
col1, col2 = st.columns(2)

with col1:
    st.subheader("Penjualan per Kategori Produk")
    sales_by_cat = df.groupby('category')['sales_amount'].sum().sort_values(ascending=False)
    st.bar_chart(sales_by_cat)

with col2:
    st.subheader("Penjualan per Negara")
    sales_by_country = df.groupby('country')['sales_amount'].sum().sort_values(ascending=False)
    st.bar_chart(sales_by_country)

st.subheader("Tren Penjualan dari Waktu ke Waktu (Bulanan)")
# Pastikan 'order_date' adalah datetime dan dijadikan index
if pd.api.types.is_datetime64_any_dtype(df['order_date']):
    sales_over_time = df.set_index('order_date').resample('M')['sales_amount'].sum()
    st.line_chart(sales_over_time)
else:
    st.warning("Format kolom 'order_date' tidak valid untuk membuat tren waktu.")


# Tampilan Data Rinci
with st.expander("Lihat Data Rinci (Raw)"):
    st.subheader("Data Penjualan Gabungan")
    st.dataframe(df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dimensi Pelanggan")
        st.dataframe(df_customers)
    with col2:
        st.subheader("Dimensi Produk")
        st.dataframe(df_products)