import yfinance as yf
import pandas as pd
import os

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "btc_prices_full.csv")

# 获取比特币数据
btc = yf.Ticker("BTC-USD")
btc_data = btc.history(start="2024-06-01", end="2025-03-10", interval="1d")

# 选择需要的列
btc_data = btc_data[["Open", "High", "Low", "Close", "Volume"]]
btc_data.reset_index(inplace=True)

# 保存到文件
btc_data.to_csv(file_path, index=False)

# 打印路径，方便查找
print(f"数据已保存到: {file_path}")
print(btc_data.head())  # 显示前 5 行数据


