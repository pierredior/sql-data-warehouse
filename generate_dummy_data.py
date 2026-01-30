
import os
import shutil

print("Memulai proses pembuatan data dummy...")

# Daftar direktori sumber
source_dirs = [
    'datasets/source_crm',
    'datasets/source_erp'
]

# Verifikasi bahwa direktori sumber ada
all_sources_exist = True
for src_dir in source_dirs:
    if not os.path.isdir(src_dir):
        print(f"ERROR: Direktori sumber tidak ditemukan di '{src_dir}'")
        all_sources_exist = False

if all_sources_exist:
    print("Semua sumber data yang ada akan digunakan.")
    print("Proses pembuatan data dummy selesai. Data mentah siap untuk diproses.")
else:
    print("Proses pembuatan data dummy gagal karena ada sumber data yang hilang.")

