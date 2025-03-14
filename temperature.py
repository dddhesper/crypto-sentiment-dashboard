import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Data
file_path = "/Users/hesperdu/Desktop/project1/finalproject/google_news_data.csv"
df = pd.read_csv(file_path)

# Compute Sentiment Score
sentiment_score = df["Sentiment Score"].astype(float).mean()

# **Layout: 分成两列，左边调节情绪值，右边放温度计**
col1, col2 = st.columns([1, 1.5])  # 让温度计宽一点，防止太瘦

with col1:
    st.markdown("### 🎛 Adjust Sentiment Score")
    sentiment_score = st.slider("", -1.0, 1.0, sentiment_score, 0.01)

# **Color function**
def get_color(score):
    if score < -0.2:
        return "red"
    elif score > 0.2:
        return "green"
    return "yellow"

color = get_color(sentiment_score)

# **Plot Temperature Gauge**
fig, ax = plt.subplots(figsize=(1, 2.5))  # **缩短高度，避免太长**

# Draw the thermometer outline
ax.plot([0, 0], [-1, 1], color='black', linewidth=4)
ax.scatter(0, -1.05, s=150, color='black', edgecolor='white', linewidth=2, alpha=0.8)  # 底部圆圈

# **Glass tube effect** (Background gradient)
ax.fill_betweenx(y=[-1, 1], x1=-0.1, x2=0.1, color="lightgray", alpha=0.3)

# **Gradient Fill** (Sentiment level)
ax.fill_betweenx(y=[-1, sentiment_score], x1=-0.1, x2=0.1, color=color, alpha=0.8)

# **Glow Effect**
ax.scatter(0, sentiment_score, s=150, color=color, edgecolor='white', linewidth=2, alpha=0.9)  # 顶部指示点

# Text annotation
ax.text(0, sentiment_score, f"{sentiment_score:.2f}", fontsize=10, ha='center', va='center', color="black", fontweight="bold")

# Hide ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

with col2:
    st.markdown("### 🔥 Bitcoin Sentiment Thermometer")
    st.pyplot(fig)

st.write(f"**Current Sentiment Score: {sentiment_score:.2f}**")
