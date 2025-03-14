import requests
import pandas as pd

# 你的 GNews API Key（免费申请）
gnews_api_key = "YOUR_GNEWS_API_KEY"

# API URL
url = f"https://gnews.io/api/v4/search?q=cryptocurrency&lang=en&from=2024-06-01&to=2025-03-14&apikey={gnews_api_key}"

# 发送请求
response = requests.get(url)
data = response.json()

if response.status_code == 200:
    df = pd.DataFrame(data["articles"])
    df.to_csv("/Users/hesperdu/Desktop/project1/finalproject/gnews_crypto_news.csv", index=False)
    print(f"✅ 成功获取 {len(df)} 篇新闻")
else:
    print(f"❌ API 请求失败: {response.status_code}, {response.text}")
