import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# 初始化 VADER 分析器
analyzer = SentimentIntensityAnalyzer()

# 读取数据（假设 CSV 文件包含 'date' 和 'text' 列）
input_csv = "crypto_news_reddit.csv"  # 请替换为你的文件名
df = pd.read_csv(input_csv)

# 确保 'date' 是日期格式
df['date'] = pd.to_datetime(df['date'])

# 计算每条文本的情绪得分
def get_sentiment_score(text):
    score = analyzer.polarity_scores(str(text))  # 确保 text 是字符串
    return score['compound']  # 取综合得分（-1 到 1）

df['sentiment_score'] = df['text'].apply(get_sentiment_score)

# 按日期计算平均情绪得分
sentiment_trend = df.groupby('date')['sentiment_score'].mean().reset_index()

# 保存结果
output_csv = "crypto_sentiment_scores.csv"
sentiment_trend.to_csv(output_csv, index=False)
print(f"情绪分析完成，结果已保存到 {output_csv}")

# 绘制情绪趋势图
plt.figure(figsize=(12, 6))
sns.lineplot(x='date', y='sentiment_score', data=sentiment_trend, marker='o')
plt.axhline(0, color='gray', linestyle='--')  # 0 轴表示中性情绪
plt.title("Cryptocurrency Sentiment Trend (VADER Analysis)")
plt.xlabel("Date")
plt.ylabel("Sentiment Score (-1 to 1)")
plt.xticks(rotation=45)
plt.show()
