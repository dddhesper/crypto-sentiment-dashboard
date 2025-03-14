import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# **Step 1: Load Data**
df_fng = pd.read_csv("filtered_fng.csv")
df_fng["timestamp"] = pd.to_datetime(df_fng["timestamp"])
df_fng["timestamp"] = df_fng["timestamp"].dt.tz_localize(None)

# 获取多个币种的数据
def get_crypto_data(ticker):
    crypto = yf.Ticker(ticker)
    df = crypto.history(period="6mo").reset_index()
    df["timestamp"] = pd.to_datetime(df["Date"])
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    df["Symbol"] = ticker  # 记录币种
    return df

# 加载 BTC, ETH, DOGE, XRP 数据
df_btc = get_crypto_data("BTC-USD")
df_eth = get_crypto_data("ETH-USD")
df_doge = get_crypto_data("DOGE-USD")
df_xrp = get_crypto_data("XRP-USD")

# 合并所有币种数据
df_all_crypto = pd.concat([df_btc, df_eth, df_doge, df_xrp], ignore_index=True)

# 只合并 BTC 数据
df_merged = pd.merge(df_fng, df_btc, on="timestamp", how="inner")

# **Step 2: Time Selection**
st.sidebar.subheader("📅 Select Time Range")
start_date, end_date = st.slider(
    "Select Date Range",
    min_value=df_merged["timestamp"].min().to_pydatetime(),
    max_value=df_merged["timestamp"].max().to_pydatetime(),
    value=(df_merged["timestamp"].min().to_pydatetime(), df_merged["timestamp"].max().to_pydatetime()),
    format="YYYY-MM-DD"
)

df_filtered = df_merged[(df_merged["timestamp"] >= pd.Timestamp(start_date)) & (df_merged["timestamp"] <= pd.Timestamp(end_date))]

# **Step 3: Interactive Dashboard**
if df_filtered.empty:
    st.warning("⚠️ No data available for the selected time range. Please adjust your selection.")
else:
    st.success("✅ Data successfully loaded!")

    # **🚀 Tabs for Different Visualizations**
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Price Trends", "🔥 Sentiment Analysis", "📊 Price vs Sentiment", "📊 Trading Volume", "🕵️‍♂️ Crypto Fear & Greed Radar"])

    with tab1:
        st.subheader("📈 Bitcoin Price vs. Fear & Greed Index")
        fig_combined = go.Figure()
        fig_combined.add_trace(go.Scatter(x=df_filtered["timestamp"], y=df_filtered["Close"], mode="lines+markers",
                                          name="Bitcoin Price (USD)", yaxis="y1"))
        fig_combined.add_trace(go.Scatter(x=df_filtered["timestamp"], y=df_filtered["value"], mode="lines+markers",
                                          name="Fear & Greed Index", yaxis="y2"))
        fig_combined.update_layout(
            title="Bitcoin Price vs. Fear & Greed Index",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Bitcoin Price (USD)", side="left"),
            yaxis2=dict(title="Fear & Greed Index", overlaying="y", side="right"),
            legend=dict(x=0, y=1)
        )
        st.plotly_chart(fig_combined, use_container_width=True)

    with tab2:
        st.subheader("🔥 Bitcoin Sentiment Thermometer")
        latest_fng = df_filtered["value"].iloc[-1]

        def draw_thermometer(fng_value):
            fig, ax = plt.subplots(figsize=(0.3, 1))  # 🔥 进一步缩窄温度计宽度
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 100)
            ax.set_xticks([])
            ax.set_yticks([0, 25, 50, 75, 100])
            ax.set_yticklabels(["😱 Extreme Fear", "😨 Fear", "😐 Neutral", "😊 Greed", "🚀 Extreme Greed"], fontsize=3)

            cmap = plt.get_cmap("RdYlGn")
            norm = plt.Normalize(0, 100)
            color = cmap(norm(fng_value))

            ax.axhline(y=fng_value, color='black', linewidth=2)
            ax.fill_betweenx([0, fng_value], 0.4, 0.6, color=color)

            ax.text(0.5, fng_value, f"{fng_value:.0f}", ha='center', fontsize=7, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='black'))  

            st.pyplot(fig)

        st.write(f"📢 **Current Market Sentiment: {latest_fng}**")

        selected_sentiment = st.slider("Select Sentiment Level", 0, 100, int(latest_fng))

        df_filtered_sentiment = df_filtered[
            (df_filtered["value"] >= selected_sentiment - 1) &
            (df_filtered["value"] <= selected_sentiment + 1)
        ]

        draw_thermometer(selected_sentiment)

        if df_filtered_sentiment.empty:
            st.warning(f"No Bitcoin price data available for Sentiment Level {selected_sentiment}. Try selecting a different value.")
        else:
            fig_sentiment = px.scatter(
                df_filtered_sentiment, 
                x="value", 
                y="Close", 
                color="value",
                hover_data=["timestamp", "Volume"],
                title=f"Bitcoin Price when Sentiment is {selected_sentiment}",
                color_continuous_scale="RdYlGn",
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)

    with tab3:
        st.subheader("📊 Bitcoin Price vs. Fear & Greed Index (Interactive)")
        fig_scatter = px.scatter(
            df_filtered,
            x="value",
            y="Close",
            color="value",
            hover_data=["timestamp", "Volume"],
            color_continuous_scale="RdYlGn",
            title="Bitcoin Price vs. Fear & Greed Index",
            labels={"value": "Fear & Greed Index", "Close": "Bitcoin Price (USD)"},
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab4:
        st.subheader("📊 Trading Volume Analysis")
        selected_symbol = st.selectbox("Select Cryptocurrency", ["BTC-USD", "ETH-USD", "DOGE-USD", "XRP-USD"])
        df_filtered_crypto = df_all_crypto[df_all_crypto["Symbol"] == selected_symbol]

        fig_volume = px.line(
            df_filtered_crypto, 
            x="timestamp", 
            y="Volume", 
            title=f"{selected_symbol} Trading Volume Over Time",
            labels={"Volume": "Trading Volume"},
        )
        st.plotly_chart(fig_volume, use_container_width=True)

    with tab5:
        st.subheader("🕵️‍♂️ Cryptocurrency Fear & Greed Radar")

        latest_values = {
            "BTC": df_btc["Close"].iloc[-1],
            "ETH": df_eth["Close"].iloc[-1],
            "DOGE": df_doge["Close"].iloc[-1],
            "XRP": df_xrp["Close"].iloc[-1]
        }

        categories = list(latest_values.keys())
        values = list(latest_values.values())

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name="Crypto Prices"
        ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title="Cryptocurrency Fear & Greed Index Comparison"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
