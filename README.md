Project Documentation

1. Data Management 

Data Sources
The data sources used in this project include:

Bitcoin & Altcoin Price Data: Collected using yfinance for (BTC-USD, ETH-USD, DOGE-USD)
Fear & Greed Index: Historical data from (filtered_fng.csv)
Cryptocurrency Trading Volume: Obtained from yfinance
Data Cleaning Process
Standardized all timestamps to UTC format
Handled NaN values by removing missing dates in price data
Filtered data to align with the Fear & Greed Index time range
Normalized different cryptocurrency datasets for integration
Sampling Methodology
Time Range: Data from June 2024 to March 2025
Data Sampling: Daily closing price (Close Price) selected for analysis
Trading Volume Data: 24-hour total trading volume used to ensure stability
2. Methodology Explanation 

Visualization Selection Rationale
This project employs multiple visualization techniques:

Line Chart - Displays Bitcoin price trends
Scatter Plot - Correlates market sentiment with Bitcoin price
Radar Chart - Compares market sentiment across different cryptocurrencies
Thermometer Visualization - Illustrates changes in the Fear & Greed Index
Interactive Slider - Allows users to select time ranges for analysis
Data Preparation Decisions
Bitcoin Data: Retained only closing price (Close Price) and trading volume (Volume)
Fear & Greed Index: Aligned timestamps to match different datasets
Additional Cryptocurrencies: Included ETH and DOGE to provide a broader market perspective
3. Critical Analysis 

Self-Critique 
Radar Chart Readability Issue: Since Bitcoin’s price is significantly higher than other cryptocurrencies, the radar chart makes the other assets nearly invisible. This suggests that the radar chart might not be the best option for comparison. Alternative visualizations such as stacked bar charts or normalized data representations could improve clarity.
Limited Sentiment Data: Currently, the Fear & Greed Index is the sole metric representing market sentiment. While it is widely recognized, it does not fully capture the complexity of the crypto market. Incorporating social media sentiment analysis (e.g., Reddit, Twitter) could provide a more comprehensive view, but API limitations prevented integration.
Limited Time Range: The dataset covers only nine months, restricting long-term trend analysis.
Future Improvements
Enhancing Data Visualization: Future iterations may explore more suitable visualizations for market share and cryptocurrency comparisons, such as stacked bar charts or normalized line charts.
Expanding Sentiment Analysis: Integrating VADER or TextBlob for Twitter and Reddit sentiment analysis could enhance the depth of market sentiment insights.
Extending the Data Range: Acquiring data over a more extended period would allow for better long-term trend analysis of market behaviors and investor psychology.