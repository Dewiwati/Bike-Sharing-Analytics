import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #F0F4F8; }
    [data-testid="stSidebar"]          { background-color: #1E3A5F; }
    [data-testid="stSidebar"] * h1,
    [data-testid="stSidebar"] * h2,
    [data-testid="stSidebar"] * h3,
    [data-testid="stSidebar"] * p,
    [data-testid="stSidebar"] * label { color: #FFFFFF !important; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1E3A5F; }
    .metric-label { font-size: 0.85rem; color: #666; margin-top: 4px; }
    h1 { color: #1E3A5F !important; }
    h2, h3 { color: #1E3A5F !important; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    day_df  = pd.read_csv("dashboard/main_data.csv",  parse_dates=["dteday"])
    hour_df = pd.read_csv("dashboard/hour_data.csv", parse_dates=["dteday"])
    return day_df, hour_df

day_df, hour_df = load_data()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚲 Bike Sharing\n### Dashboard Analisis")
    st.markdown("---")

    st.markdown("### 📅 Filter Tanggal")
    min_date = day_df["dteday"].min().date()
    max_date = day_df["dteday"].max().date()
    date_range = st.date_input(
        "Pilih rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")

    st.markdown("### 🌤️ Filter Musim")
    season_options = ["Semua"] + list(day_df["season_label"].unique())
    selected_season = st.selectbox("Pilih Musim", season_options)

    st.markdown("---")
    st.markdown("**Sumber Data:**\nCapital Bikeshare\nWashington D.C., 2011–2012")
    st.markdown("**Dibuat oleh:** Dewi Wati")

# ─── Filter Data ──────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start, end = pd.Timestamp(min_date), pd.Timestamp(max_date)

filtered_day = day_df[(day_df["dteday"] >= start) & (day_df["dteday"] <= end)]
if selected_season != "Semua":
    filtered_day = filtered_day[filtered_day["season_label"] == selected_season]

filtered_hour = hour_df[(hour_df["dteday"] >= start) & (hour_df["dteday"] <= end)]
if selected_season != "Semua":
    filtered_hour = filtered_hour[filtered_hour["season_label"] == selected_season]

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Analisis pola peminjaman sepeda Capital Bikeshare, Washington D.C. (2011–2012)")
st.markdown("---")

# ─── KPI Metrics ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_rentals = filtered_day["cnt"].sum()
avg_daily     = filtered_day["cnt"].mean()
total_days    = len(filtered_day)
peak_day_val  = filtered_day["cnt"].max()

with col1:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>🚴 {total_rentals:,.0f}</div>
        <div class='metric-label'>Total Peminjaman</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>📊 {avg_daily:,.0f}</div>
        <div class='metric-label'>Rata-rata / Hari</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>📅 {total_days:,}</div>
        <div class='metric-label'>Jumlah Hari</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class='metric-card'>
        <div class='metric-value'>🏆 {peak_day_val:,.0f}</div>
        <div class='metric-label'>Peminjaman Tertinggi / Hari</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Section 1: Musim & Cuaca ─────────────────────────────────────────────────
st.markdown("## 📌 Pertanyaan 1: Pengaruh Musim & Cuaca")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### Rata-rata Peminjaman per Musim")
    season_order   = ["Springer", "Summer", "Fall", "Winter"]
    season_palette = {"Springer": "#4CAF50", "Summer": "#FF9800", "Fall": "#F44336", "Winter": "#2196F3"}

    season_avg = filtered_day.groupby("season_label")["cnt"].mean().reindex(
        [s for s in season_order if s in filtered_day["season_label"].unique()]
    )

    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    colors = [season_palette.get(s, "#999") for s in season_avg.index]
    bars = ax1.bar(season_avg.index, season_avg.values,
                   color=colors, edgecolor="white", linewidth=1.5, width=0.6)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 f"{bar.get_height():,.0f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")
    ax1.set_ylabel("Rata-rata Peminjaman Harian")
    ax1.set_xlabel("Musim")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.set_facecolor("#FAFAFA")
    fig1.patch.set_facecolor("#FAFAFA")
    st.pyplot(fig1)
    plt.close()

with col_b:
    st.markdown("### Rata-rata Peminjaman per Kondisi Cuaca")
    weather_order  = ["Clear", "Mist/Cloudy", "Light Rain/Snow"]
    weather_colors = ["#FFD700", "#90A4AE", "#4FC3F7"]

    weather_data = filtered_day[filtered_day["weather_label"].isin(weather_order)]
    weather_avg  = weather_data.groupby("weather_label")["cnt"].mean().reindex(
        [w for w in weather_order if w in weather_data["weather_label"].unique()]
    )

    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    bars2 = ax2.bar(weather_avg.index, weather_avg.values,
                    color=weather_colors[:len(weather_avg)], edgecolor="white", linewidth=1.5)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 f"{bar.get_height():,.0f}", ha="center", va="bottom",
                 fontsize=10, fontweight="bold")
    ax2.set_ylabel("Rata-rata Peminjaman Harian")
    ax2.set_xlabel("Kondisi Cuaca")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.set_facecolor("#FAFAFA")
    fig2.patch.set_facecolor("#FAFAFA")
    st.pyplot(fig2)
    plt.close()

with st.expander("💡 Insight: Pengaruh Musim & Cuaca"):
    st.markdown("""
    - **Fall (Gugur)** memiliki rata-rata peminjaman tertinggi (5.644/hari) karena suhu yang nyaman.
    - **Springer (Semi)** memiliki rata-rata terendah (2.604/hari) — selisih lebih dari 2× lipat.
    - Cuaca **Clear** menghasilkan peminjaman tertinggi (4.877/hari).
    - **Light Rain/Snow** menurunkan peminjaman hingga ~63% menjadi 1.803/hari.
    - Operator sebaiknya memaksimalkan ketersediaan armada pada musim Fall dengan cuaca cerah, dan menyiapkan strategi diskon atau fleksibilitas saat cuaca buruk.
    """)

st.markdown("---")

# ─── Section 2: Pola Jam ──────────────────────────────────────────────────────
st.markdown("## 📌 Pertanyaan 2: Pola Peminjaman per Jam")

fig3, ax3 = plt.subplots(figsize=(13, 5))

hourly_wd  = filtered_hour[filtered_hour["workingday"] == 1].groupby("hr")["cnt"].mean()
hourly_hol = filtered_hour[filtered_hour["workingday"] == 0].groupby("hr")["cnt"].mean()

ax3.plot(hourly_wd.index,  hourly_wd.values,  marker="o", linewidth=2.5, color="#1565C0",
         label="Hari Kerja", markersize=5)
ax3.plot(hourly_hol.index, hourly_hol.values, marker="s", linewidth=2.5, color="#E53935",
         label="Hari Libur/Weekend", markersize=5, linestyle="--")
ax3.fill_between(hourly_wd.index,  hourly_wd.values,  alpha=0.08, color="#1565C0")
ax3.fill_between(hourly_hol.index, hourly_hol.values, alpha=0.08, color="#E53935")

# Anotasi jam puncak hari kerja
if not hourly_wd.empty:
    for hr, label in [(8, "Puncak\n08:00"), (17, "Puncak\n17:00")]:
        if hr in hourly_wd.index:
            val = hourly_wd[hr]
            ax3.annotate(f"{label}\n({val:.0f})",
                         xy=(hr, val), xytext=(hr + 0.8, val + 20),
                         fontsize=9, color="#1565C0", fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.5))

ax3.set_title("Pola Peminjaman Sepeda per Jam: Hari Kerja vs Hari Libur/Weekend",
              fontsize=13, fontweight="bold")
ax3.set_xlabel("Jam (0–23)", fontsize=11)
ax3.set_ylabel("Rata-rata Jumlah Peminjaman", fontsize=11)
ax3.set_xticks(range(0, 24))
ax3.legend(fontsize=11)
ax3.grid(True, linestyle="--", alpha=0.4)
ax3.spines[["top", "right"]].set_visible(False)
ax3.set_facecolor("#FAFAFA")
fig3.patch.set_facecolor("#FAFAFA")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
st.pyplot(fig3)
plt.close()

with st.expander("💡 Insight: Pola Jam"):
    st.markdown("""
    - **Hari Kerja:** Dua puncak tajam — **jam 08:00 (477)** dan **jam 17:00 (525)**. Pola *commuter*.
    - **Hari Libur/Weekend:** Puncak tunggal di **jam 12:00–13:00**. Pola *rekreasi* yang lebih santai.
    - Pastikan sepeda tersedia di stasiun perkantoran pukul 07:30 & 16:30 di hari kerja.
    - Distribusikan sepeda ke jalur rekreasi pada hari libur/weekend.
    """)

st.markdown("---")

# ─── Section 3: Clustering ────────────────────────────────────────────────────
st.markdown("## 📌 Analisis Lanjutan: Demand Clustering")
st.markdown("Pengelompokan hari berdasarkan intensitas peminjaman menggunakan metode **binning** (quantile 33/66).")

cluster_order   = ["Low Demand", "Medium Demand", "High Demand"]
cluster_palette = {"Low Demand": "#EF5350", "Medium Demand": "#FFA726", "High Demand": "#66BB6A"}

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown("### Jumlah Hari per Cluster")
    cluster_counts = filtered_day["demand_cluster"].value_counts().reindex(
        [c for c in cluster_order if c in filtered_day["demand_cluster"].unique()]
    )

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    bars4 = ax4.bar(cluster_counts.index, cluster_counts.values,
                    color=[cluster_palette[c] for c in cluster_counts.index],
                    edgecolor="white", linewidth=1.5)
    for bar in bars4:
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 str(int(bar.get_height())), ha="center", va="bottom",
                 fontsize=11, fontweight="bold")
    ax4.set_ylabel("Jumlah Hari")
    ax4.set_xlabel("Cluster")
    ax4.spines[["top", "right"]].set_visible(False)
    ax4.set_facecolor("#FAFAFA")
    fig4.patch.set_facecolor("#FAFAFA")
    st.pyplot(fig4)
    plt.close()

with col_c2:
    st.markdown("### Rata-rata Suhu per Cluster (°C)")
    temp_by_cluster = filtered_day.groupby("demand_cluster")["temp_celsius"].mean().reindex(
        [c for c in cluster_order if c in filtered_day["demand_cluster"].unique()]
    )

    fig5, ax5 = plt.subplots(figsize=(6, 4))
    bars5 = ax5.barh(temp_by_cluster.index, temp_by_cluster.values,
                     color=[cluster_palette[c] for c in temp_by_cluster.index],
                     edgecolor="white", linewidth=1.5)
    for i, v in enumerate(temp_by_cluster.values):
        ax5.text(v + 0.2, i, f"{v:.1f}°C", va="center", fontweight="bold", fontsize=11)
    ax5.set_xlabel("Suhu (°C)")
    ax5.spines[["top", "right"]].set_visible(False)
    ax5.set_facecolor("#FAFAFA")
    fig5.patch.set_facecolor("#FAFAFA")
    st.pyplot(fig5)
    plt.close()

with st.expander("💡 Insight: Demand Clustering"):
    st.markdown("""
    - 🔴 **Low Demand** → Terjadi pada suhu rendah (~11°C). Armada minimal, jadwalkan maintenance.
    - 🟡 **Medium Demand** → Suhu sedang (~19°C). Armada normal, monitoring rutin.
    - 🟢 **High Demand** → Suhu hangat (~25°C). Armada maksimal, penambahan staf.
    """)

st.markdown("---")
st.markdown("*Dashboard dibuat untuk Proyek Analisis Data — Dicoding | Data: Capital Bikeshare 2011–2012*")
st.markdown("*Nama: Dewi Wati | Email: CDCC351D6X1980@student.devacademy.id*")