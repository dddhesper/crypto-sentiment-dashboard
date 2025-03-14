import praw
import pandas as pd

# ✅ 1. 设定 Reddit API 认证
reddit = praw.Reddit(
    client_id="C5PmC1w1rxgrETrvdrsYPQ",
    client_secret="你的_CLIENT_SECRET",
    user_agent="CryptoSentimentApp v1.0 (by /u/你的Reddit用户名)",
)

# ✅ 2. 设定抓取的 subreddit 列表
crypto_subreddits = ["cryptocurrency", "Bitcoin", "CryptoMarkets", "dogecoin", "ethereum"]

all_posts = []

# ✅ 3. 循环抓取多个 subreddits 的数据
for subreddit_name in crypto_subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    print(f"📡 Fetching posts from r/{subreddit_name}...")
    
    for post in subreddit.hot(limit=500):  # ✅ 获取 500 条数据，增加数据量
        all_posts.append({
            "subreddit": subreddit_name,
            "title": post.title,
            "score": post.score,  # 文章热度
            "num_comments": post.num_comments,  # 评论数量
            "created_utc": post.created_utc,  # 创建时间
            "url": post.url  # 文章链接
        })

# ✅ 4. 转换成 Pandas DataFrame 并存储为 CSV
df = pd.DataFrame(all_posts)
df.to_csv("/Users/hesperdu/Desktop/project1/finalproject/crypto_reddit_sentiment.csv", index=False, encoding="utf-8")

print("✅ 成功抓取 Reddit 数据，已保存到 crypto_reddit_sentiment.csv！")
