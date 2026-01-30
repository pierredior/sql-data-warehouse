import pandas as pd
import sqlalchemy
import os
import sqlite3

DB_NAME = 'dwh.db'

def run_sql_script(filename, conn):
    """Membaca dan menjalankan skrip SQL dari sebuah file, memisahkan berdasarkan semicolon."""
    with open(filename, 'r') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    conn.execute(sqlalchemy.text(command))
                    print(f"  >> Perintah berhasil dijalankan dari {filename}: {command.splitlines()[0]}...")
                except Exception as e:
                    # Jangan cetak error jika itu hanya karena tabel sudah ada atau belum ada
                    if "already exists" not in str(e) and "no such table" not in str(e):
                        print(f"  >> Gagal menjalankan perintah dari {filename}: {command.splitlines()[0]}...\n{e}")

def load_bronze_layer(engine):
    """Memuat data dari CSV ke tabel Bronze."""
    print("\nMemulai loading Bronze Layer...")
    
    # 1. Membuat tabel bronze dari DDL yang sudah diperbaiki
    with engine.connect() as conn:
        run_sql_script('scripts/bronze/ddl_bronze.sql', conn)

    # 2. Definisi mapping file CSV ke tabel
    csv_to_table_map = {
        'datasets/source_crm/cust_info.csv': 'bronze_crm_cust_info',
        'datasets/source_crm/prd_info.csv': 'bronze_crm_prd_info',
        'datasets/source_crm/sales_details.csv': 'bronze_crm_sales_details',
        'datasets/source_erp/CUST_AZ12.csv': 'bronze_erp_cust_az12',
        'datasets/source_erp/LOC_A101.csv': 'bronze_erp_loc_a101',
        'datasets/source_erp/PX_CAT_G1V2.csv': 'bronze_erp_px_cat_g1v2',
    }

    # 3. Memuat data dari CSV
    for csv_path, table_name in csv_to_table_map.items():
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Ganti nama kolom jika ada spasi
            df.columns = df.columns.str.strip()
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"  >> Data dari {csv_path} dimuat ke {table_name}")
        else:
            print(f"  >> PERINGATAN: File tidak ditemukan: {csv_path}")
            
    print("Loading Bronze Layer selesai.")

def load_silver_layer(engine):
    """Memuat data dari Bronze ke Silver setelah transformasi."""
    print("\nMemulai loading Silver Layer...")
    
    # Langkah 1: Buat tabel silver menggunakan SQLAlchemy (DDL aman)
    with engine.connect() as conn:
        run_sql_script('scripts/silver/ddl_silver.sql', conn)
    print("  >> Skema Silver berhasil dibuat.")

    # Langkah 2: Gunakan pustaka sqlite3 asli untuk menjalankan skrip transformasi
    # Ini untuk memastikan penanganan transaksi yang benar yang mungkin menjadi masalah
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        with open('scripts/silver/proc_load_silver.sql', 'r') as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("  >> Skrip transformasi Silver berhasil dijalankan dan di-commit.")
    except Exception as e:
        print(f"  >> Gagal saat menjalankan skrip transformasi Silver: {e}")

    print("Loading Silver Layer selesai.")

def create_gold_layer(engine):
    """Membuat Views untuk Gold Layer."""
    print("\nMemulai pembuatan Gold Layer...")
    with engine.connect() as conn:
        run_sql_script('scripts/gold/ddl_gold.sql', conn)
    print("Pembuatan Gold Layer selesai.")

def main():
    """Fungsi utama untuk menjalankan pipeline ETL."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Database '{DB_NAME}' yang ada telah dihapus.")

    engine = sqlalchemy.create_engine(f'sqlite:///{DB_NAME}')
    
    print("\nMemulai pipeline ETL...")
    
    load_bronze_layer(engine)
    load_silver_layer(engine)
    create_gold_layer(engine)
    
    print("\nPipeline ETL berhasil diselesaikan!")

if __name__ == '__main__':
    main()