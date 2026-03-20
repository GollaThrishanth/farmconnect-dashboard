import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="FarmConnect Dashboard", layout="wide")
st.title("🌾 FarmConnect Advanced Smart Dashboard")

# -----------------------------
# LOAD & CLEAN DATA
# -----------------------------
df_raw = pd.read_csv("data.csv, skiprows=2)

# Pick important columns
df = df_raw.iloc[:, [1, 4, 5, 6, 8]].copy()

# Rename
df.columns = ["Commodity", "Price_Today", "Price_Yesterday", "Price_DayBefore", "Arrival"]

# Convert to numeric
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

# -----------------------------
# SHOW DATA
# -----------------------------
st.subheader("📊 Cleaned Data")
st.dataframe(df)

# -----------------------------
# 📈 PRICE TREND GRAPH (NEW 🔥)
# -----------------------------
st.subheader("📈 Price Trend (Last 3 Days)")

trend_df = df.melt(
    id_vars="Commodity",
    value_vars=["Price_Today", "Price_Yesterday", "Price_DayBefore"],
    var_name="Day",
    value_name="Price"
)

fig_trend = px.line(
    trend_df,
    x="Day",
    y="Price",
    color="Commodity",
    markers=True,
    title="Price Trend Over Days"
)

st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# ⚖ DEMAND vs SUPPLY
# -----------------------------
st.subheader("⚖ Demand vs Supply")

# Simple logic (hackathon smart trick)
df["Demand"] = df["Price_Today"] * 0.5
df["Supply"] = df["Arrival"]

fig_ds = px.scatter(
    df,
    x="Supply",
    y="Demand",
    size="Price_Today",
    color="Commodity",
    title="Demand vs Supply Analysis"
)

st.plotly_chart(fig_ds, use_container_width=True)

# -----------------------------
# 📊 BAR GRAPH
# -----------------------------
st.subheader("💰 Price Comparison")

fig_bar = px.bar(df, x="Commodity", y="Price_Today", color="Price_Today")
st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# 🔥 SEABORN DISTRIBUTION
# -----------------------------
st.subheader("🔥 Price Distribution")

plt.figure()
sns.histplot(df["Price_Today"], kde=True)
st.pyplot(plt)

# -----------------------------
# 🏆 TOP CROPS
# -----------------------------
st.subheader("🏆 Top 5 Crops")

top5 = df.sort_values(by="Price_Today", ascending=False).head(5)

fig_top = px.bar(top5, x="Commodity", y="Price_Today", color="Price_Today")
st.plotly_chart(fig_top, use_container_width=True)

# -----------------------------
# 🧠 INSIGHTS
# -----------------------------
st.subheader("🧠 Insights")

highest = df.loc[df["Price_Today"].idxmax()]
lowest = df.loc[df["Price_Today"].idxmin()]

st.success(f"💰 Highest Price: {highest['Commodity']} (₹{highest['Price_Today']})")
st.info(f"📉 Lowest Price: {lowest['Commodity']} (₹{lowest['Price_Today']})")

# -----------------------------
# 🔊 VOICE EXPLANATION (GAME CHANGER 🚀)
# -----------------------------
st.subheader("🔊 Voice Explanation")

summary_text = f"""
Highest priced crop is {highest['Commodity']}.
Lowest priced crop is {lowest['Commodity']}.
Prices are changing based on demand and supply.
"""

st.write(summary_text)

st.markdown(f"""
<script>
var msg = new SpeechSynthesisUtterance("{summary_text}");
window.speechSynthesis.speak(msg);
</script>
""", unsafe_allow_html=True)
