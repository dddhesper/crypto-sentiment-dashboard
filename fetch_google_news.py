from GoogleNews import GoogleNews
import pandas as pd
from textblob import TextBlob
import nltk

# 下载 NLTK 数据（首次运行时需要）
nltk.download('punkt')

# 配置 Google News
googlenews = GoogleNews(lang='en', region='US', period='7d')  # 抓取最近 7 天的新闻
googlenews.search('Bitcoin')

# 获取新闻数据
news_results = googlenews.result()
news_data = []

for news in news_results:
    title = news['title']
    link = news['link']
    content = news['desc']
    
    # 情绪分析
    analysis = TextBlob(content)
    sentiment_score = analysis.sentiment.polarity  # 介于 -1（负面）到 1（正面）之间
    sentiment = "Positive" if sentiment_score > 0.1 else "Negative" if sentiment_score < -0.1 else "Neutral"
    
    news_data.append([title, content, link, sentiment_score, sentiment])

# 存入 DataFrame
df = pd.DataFrame(news_data, columns=["Title", "Content", "Link", "Sentiment Score", "Sentiment"])

# 存为 CSV
df.to_csv("google_news_data.csv", index=False)

print("✅ Google News 数据获取完成！")
print(df.head())  # 预览前几行
