import yfinance as yf
import pandas as pd

# 需要下载的币种
symbols = ["BTC-USD", "ETH-USD", "XRP-USD", "DOGE-USD"]

# 设定时间范围
start_date = "2024-06-01"
end_date = "2025-03-14"

# 下载数据并保存
for symbol in symbols:
    print(f"📥 Downloading {symbol} data...")

    # 获取数据
    df = yf.download(symbol, start=start_date, end=end_date)

    # 检查数据是否为空
    if df.empty:
        print(f"⚠️ WARNING: No data found for {symbol}!")
        continue  # 跳过当前币种，继续下一个

    # 处理数据格式
    df = df.reset_index()
    df["symbol"] = symbol  # 添加币种名称列
    df.rename(columns={"Date": "timestamp", "Close": "price", "Volume": "trading_volume"}, inplace=True)

    # 生成文件路径
    csv_filename = f"/Users/hesperdu/Desktop/project1/finalproject/{symbol.replace('-USD', '')}_data.csv"

    # 保存为 CSV
    df.to_csv(csv_filename, index=False)
    
    print(f"✅ Data for {symbol} saved to {csv_filename}")

print("🎉 All cryptocurrency data has been downloaded and saved successfully!")
