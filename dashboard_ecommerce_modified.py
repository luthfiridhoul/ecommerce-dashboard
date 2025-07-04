
import streamlit as st

st.set_page_config(
    page_title="E-Commerce Insight Board",
    page_icon="📦",
    layout="wide"
)

import pandas as pd
import plotly.express as px

# --- GAYA TAMBAHAN ---
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .st-b6, .st-cq, .st-emotion-cache-16txtl3 {
        background-color: #1c1c1c !important;
        border-radius: 12px;
    }
    .stMetric {
        background-color: #262626;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #333333;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_customer_data_large.csv")
    df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
    df['Month'] = df['Purchase Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# --- HEADER ---
st.title("📊 E-Commerce Customer Dashboard")
st.caption("Visualisasi data transaksi dan perilaku pelanggan - Dibuat oleh Luthfi")

# --- FILTER SAMPING ---
st.sidebar.title("🔍 Filter Data")

category = st.sidebar.multiselect("Kategori Produk:", df["Product Category"].unique(), default=df["Product Category"].unique())
method = st.sidebar.selectbox("Metode Pembayaran:", ["All"] + list(df["Payment Method"].unique()))
show_gender = st.sidebar.checkbox("Filter Berdasarkan Gender", value=False)

df_filtered = df[df["Product Category"].isin(category)]
if method != "All":
    df_filtered = df_filtered[df_filtered["Payment Method"] == method]
if show_gender:
    selected_gender = st.sidebar.radio("Pilih Gender:", df["Gender"].unique())
    df_filtered = df_filtered[df_filtered["Gender"] == selected_gender]

# --- METRIK KUNCI ---
st.subheader("📈 Statistik Penjualan")
total = df_filtered["Total Purchase Amount"].sum()
customers = df_filtered["Customer ID"].nunique()
avg_price = df_filtered["Product Price"].mean()

m1, m2, m3 = st.columns(3)
m1.metric("Total Penjualan", f"${total:,.0f}")
m2.metric("Jumlah Pelanggan Unik", f"{customers}")
m3.metric("Rata-rata Harga Produk", f"${avg_price:.2f}")

# --- ANALISIS SINGKAT ---
st.subheader("🧠 Insight Pelanggan")
c1, c2 = st.columns(2)
most_returned = df_filtered["Returns"].mean() * 100
top_category = df_filtered.groupby("Product Category")["Total Purchase Amount"].sum().idxmax()

c1.info(f"📦 Return Rate Rata-rata: {most_returned:.2f}%")
c2.success(f"🏆 Kategori Terlaris: {top_category}")

# --- VISUALISASI ---
st.markdown("### 📊 Visualisasi Data")
cat_sales = df_filtered.groupby("Product Category")["Total Purchase Amount"].sum().reset_index()
monthly = df_filtered.groupby("Month")["Total Purchase Amount"].sum().reset_index()

fig_cat = px.pie(cat_sales, names="Product Category", values="Total Purchase Amount", title="Proporsi Penjualan per Kategori", template="plotly_dark")
fig_month = px.area(monthly, x="Month", y="Total Purchase Amount", title="Tren Penjualan Bulanan", template="plotly_dark")

v1, v2 = st.columns(2)
v1.plotly_chart(fig_cat, use_container_width=True)
v2.plotly_chart(fig_month, use_container_width=True)

# --- DATAFRAME ---
with st.expander("🧾 Tampilkan Data Tersaring"):
    st.dataframe(df_filtered.head(100), use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<center><small> Luthfi Ridhoul - DiBimbing DS32B| Dibuat dengan Streamlit</small></center>", unsafe_allow_html=True)
