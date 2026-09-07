# E-Commerce Performance Dashboard

Dokumentasi proyek analisis data e-commerce berbasis dataset publik. Proyek ini mencakup alur kerja analisis data secara menyeluruh, mulai dari perumusan pertanyaan bisnis SMART, _Data Wrangling_, _Exploratory Data Analysis_ (EDA), hingga visualisasi dan pembuatan _dashboard_ interaktif menggunakan Streamlit.

---

## Pertanyaan Bisnis (SMART Questions)

Proyek analisis data ini bertujuan untuk menjawab tiga pertanyaan bisnis utama:

1. **Pertanyaan 1**: Kategori produk apa yang menghasilkan total pendapatan (_revenue_) tertinggi selama periode tahun 2017 hingga 2018?
2. **Pertanyaan 2**: Bagaimana tingkat kepuasan pelanggan (_review score_) berdasarkan rata-rata durasi pengiriman pesanan (_delivery time_) di setiap negara bagian (_customer state_)?
3. **Pertanyaan 3**: Metode pembayaran apa yang paling dominan digunakan oleh pelanggan berdasarkan total nilai transaksi?

---

## Ringkasan Alur Kerja Analisis Data

1. **Data Wrangling**:
   - **Gathering Data**: Memuat 7 tabel dataset e-commerce (`orders`, `customers`, `order_items`, `order_payments`, `order_reviews`, `products`, `product_category_name_translation`).
   - **Assessing Data**: Mengidentifikasi _missing values_ pada tanggal pengiriman, inkonsistensi tipe data string pada kolom _timestamp_, serta translasi kategori produk.
   - **Cleaning Data**: Mengonversi kolom tanggal ke format `datetime`, menerjemahkan nama kategori ke bahasa Inggris, menghapus transaksi yang dibatalkan/belum dikirim untuk analisis logistik, serta menambahkan fitur turunan `delivery_time_days` dan `is_delayed`.

2. **Exploratory Data Analysis (EDA)**:
   - Menggabungkan seluruh tabel ke dalam `master_df`.
   - Melakukan agregasi data untuk menghitung total pendapatan per kategori, rata-rata durasi pengiriman dan ulasan per negara bagian, serta distribusi nilai transaksi per metode pembayaran.

3. **Visualization & Explanatory Analysis**:
   - Menyajikan visualisasi _barplot_ dan _scatterplot_ untuk menjawab setiap pertanyaan bisnis.

---

## Kesimpulan & Rekomendasi Action Item

### Kesimpulan:

- **Pendapatan Kategori**: Kategori produk **health_beauty** (1.27M BRL) dan **watches_gifts** (1.21M BRL) menjadi kontributor pendapatan terbesar platform e-commerce sepanjang periode 2017–2018.
- **Performa Pengiriman & Kepuasan**: Terdapat korelasi negatif antara durasi pengiriman dan skor ulasan; negara bagian dengan rata-rata waktu pengiriman melampaui **15 hari** mengalami penurunan _review score_ hingga di bawah skala 4.0.
- **Metode Pembayaran**: Metode **credit_card** mendominasi platform dengan total nilai transaksi mencapai **15.27 juta BRL**, diikuti oleh **boleto** sebesar 3.97 juta BRL.

### Rekomendasi Action Item:

- **Optimasi Logistik**: Evaluasi dan rekrut mitra logistik lokal tambahan di negara bagian dengan waktu transit tinggi guna menekan durasi pengiriman di bawah 15 hari.
- **Manajemen Stok Unggulan**: Prioritaskan ketersediaan stok dan alokasi anggaran promosi pada kategori _top-performing_ (`health_beauty` dan `watches_gifts`).
- **Kemitraan Pembayaran**: Gandeng penyedia _credit card_ untuk program promo cicilan 0% guna mempertahankan basis pengguna utama.

---

## Struktur Direktori Proyek

```text
submission/
├── data/                                # Folder dataset mentah (CSV)
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   └── products_dataset.csv
├── dashboard/                           # Folder aplikasi dashboard
│   ├── dashboard.py                     # Skrip utama Streamlit
│   └── main_data.csv                    # Clean dataset hasil wrangling
├── notebook.ipynb                       # Jupyter / Colab Notebook analisis
├── README.md                            # Dokumentasi proyek
├── requirements.txt                     # Dependensi Python
└── url.txt                              # Link deployment Streamlit Cloud
```

## Panduan Menjalankan Dashboard Secara Lokal

1. Prasyarat & Instalasi
   Pastikan Anda telah menginstal Python (versi 3.9+). Jalankan perintah berikut di terminal/PowerShell untuk menginstal seluruh pustaka yang dibutuhkan:

```
Bash
pip install -r requirements.txt
```

1. Menjalankan Aplikasi Streamlit
   Pindahlah ke direktori proyek dan jalankan perintah Streamlit:

```
Bash
cd dashboard
streamlit run dashboard.py
```

Dashboard interaktif akan otomatis terbuka di peramban web lokal Anda (biasanya di http://localhost:8501).
