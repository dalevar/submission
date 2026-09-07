import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency
sns.set(style='dark')

# Config Halaman
st.set_page_config(
    page_title="E-Commerce Performance Dashboard",
    page_icon=":sparkles:",
    layout="wide"
)

# Function untuk Load Data
@st.cache_data
def load_data():
    # Menentukan direktori tempat file dashboard.py ini berada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path)
    datetime_cols = [
        'order_purchase_timestamp', 
        'order_approved_at', 
        'order_delivered_carrier_date', 
        'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df

master_df = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200)

st.sidebar.title("Filter & Navigasi")

min_date = master_df['order_purchase_timestamp'].min().date()
max_date = master_df['order_purchase_timestamp'].max().date()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu Transaksi',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

filtered_df = master_df[
    (master_df['order_purchase_timestamp'].dt.date >= start_date) & 
    (master_df['order_purchase_timestamp'].dt.date <= end_date)
]

# -----------------------------------------------------------------------------
# MAIN DASHBOARD METRICS
st.title("E-Commerce Performance Dashboard :sparkles:")

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = filtered_df['order_id'].nunique() if 'order_id' in filtered_df.columns else len(filtered_df)
    st.metric(label="Total Pesanan", value=f"{total_orders:,}")

with col2:
    if 'price' in filtered_df.columns:
        total_revenue = filtered_df['price'].sum()
    elif 'payment_value' in filtered_df.columns:
        total_revenue = filtered_df['payment_value'].sum()
    else:
        total_revenue = 0
    st.metric(label="Total Pendapatan", value=f"{total_revenue:,.2f} BRL")

with col3:
    if 'delivery_time_days' in filtered_df.columns:
        avg_delivery = filtered_df['delivery_time_days'].mean()
        st.metric(label="Rata-rata Pengiriman", value=f"{avg_delivery:.1f} Hari")
    else:
        st.metric(label="Rata-rata Pengiriman", value="N/A")

st.divider()

# -----------------------------------------------------------------------------
# PERTANYAAN 1: TOP 5 KATEGORI PRODUK
st.subheader("1. Top 5 Kategori Produk Berdasarkan Total Pendapatan")

val_col = 'price' if 'price' in filtered_df.columns else 'payment_value'

if val_col in filtered_df.columns and 'product_category_name_english' in filtered_df.columns:
    top_5_categories = filtered_df.groupby('product_category_name_english')[val_col].sum().nlargest(5).reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=top_5_categories, 
        x=val_col, 
        y='product_category_name_english', 
        hue='product_category_name_english',
        legend=False,
        palette='Blues_r',
        ax=ax
    )
    ax.set_title("Top 5 Kategori Produk Berdasarkan Pendapatan (BRL)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Total Pendapatan (BRL)")
    ax.set_ylabel("Kategori Produk")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)
else:
    st.warning("Kolom kategori produk atau nilai pendapatan tidak ditemukan pada dataset.")

st.divider()

# -----------------------------------------------------------------------------
# PERTANYAAN 2: DURASI PENGIRIMAN VS REVIEW SCORE
st.subheader("2. Pengaruh Rata-Rata Waktu Pengiriman Terhadap Skor Ulasan Pelanggan")

if 'customer_state' in filtered_df.columns and 'delivery_time_days' in filtered_df.columns and 'review_score' in filtered_df.columns:
    delivery_by_state = filtered_df.groupby('customer_state').agg({
        'delivery_time_days': 'mean',
        'review_score': 'mean'
    }).reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.scatterplot(
        data=delivery_by_state, 
        x='delivery_time_days', 
        y='review_score', 
        color='crimson', 
        s=100, 
        alpha=0.8,
        ax=ax2
    )
    ax2.axvline(x=15, color='gray', linestyle='--', label='Batas Pengiriman 15 Hari')
    ax2.set_title("Rata-Rata Waktu Pengiriman vs Skor Ulasan per Negara Bagian", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Rata-Rata Waktu Pengiriman (Hari)")
    ax2.set_ylabel("Rata-Rata Skor Ulasan (1–5)")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)
else:
    st.warning("Kolom pengiriman atau review score tidak ditemukan.")

st.divider()

# -----------------------------------------------------------------------------
# PERTANYAAN 3: METODE PEMBAYARAN
st.subheader("3. Distribusi Total Nilai Transaksi Berdasarkan Metode Pembayaran")

pay_val_col = 'payment_value' if 'payment_value' in filtered_df.columns else 'price'

if 'payment_type' in filtered_df.columns and pay_val_col in filtered_df.columns:
    payment_summary = filtered_df.groupby('payment_type')[pay_val_col].sum().reset_index()
    payment_summary = payment_summary.sort_values(by=pay_val_col, ascending=False)

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=payment_summary, 
        x='payment_type', 
        y=pay_val_col, 
        hue='payment_type',
        legend=False,
        palette='Blues_r',
        ax=ax3
    )
    ax3.set_title("Total Nilai Transaksi per Metode Pembayaran", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Metode Pembayaran")
    ax3.set_ylabel("Total Nilai Pembayaran (BRL)")
    ax3.grid(axis='y', linestyle='--', alpha=0.7)

    for index, row in payment_summary.iterrows():
        ax3.text(index, row[pay_val_col], f"{row[pay_val_col]/1e6:.2f}M BRL", color='black', ha="center", va="bottom")

    st.pyplot(fig3)
else:
    st.info("Kolom 'payment_type' atau nilai pembayaran tidak ditemukan pada CSV ini.")