# Quantitative Analysis on Futures

**Enhancing Trading Decisions Through Data-Driven Market Insights**

This project provides a versatile set of quantitative tools for analyzing futures price and volume data, offering a structured approach to volatility analysis, regime detection, and market structure evaluation. While this repository focuses on Crude Oil, the methodologies and tools can be applied to any asset class, including equities, FX, commodities, and fixed income.

By leveraging statistical techniques and financial market models, this framework helps traders:

- Contextualize price movements using volatility distributions and historical comparisons.
- Identify market regimes using Hurst exponent analysis to differentiate between trending vs. mean-reverting conditions, helping traders select the appropriate strategy.
- Analyze market structure via Market Profile and Volume Profile to highlight key price levels, liquidity zones, and fair value areas.

This repository serves as a quantitatively driven research framework, equipping traders with actionable insights for any instrument they wish to trade.

Sample output for research on Crude Oil: https://nbviewer.org/github/linli2492/ProjectsPortfolio/blob/main/TradingPortfolioRiskManagement/QuantAnalysisProject/Speculators%20Daily%20Crude%20Oil%2004022025.ipynb

## Volatility Analysis

- **Objective**: Compare the most recent trading session's volatility against historical distributions over 1-month, 3-month, 6-month, and 12-month timeframes.
- **Methodology**:
  - Compute daily high-low range distributions.
  - Uses Kernel Density Estimation (KDE) & histograms to visualize how the latest volatility compares to historical averages.
- **Sample Output**:
*Daily Volatility of Crude Oil as of 03/02/2025*

![Daily Volatility Sample](Images/DailyVolSample.png)

## Market Regime Detection

- **Objective**: Identify whether the asset was trending or mean-reverting the previous day.
- **Methodology**:
  - Uses the Hurst Exponent to classify price behaviour.
  - Values between 0.49 and 0.51 are classified as Random Walks.
  - Hursts > 0.51 indicate trending markets, Hurst < 0.49 indicate mean-reverting markets.
- **Application**:
This helps traders align their strategies with market conditions:
  - **Trending Markets** -> Favour breakout and momentum-based strategies.
  - **Mean-Reverting Markets** -> Favour range-bound trading and fading extremes.
  - 
**Sample Output**:
*Market Regime count and time series plot of Crude Oil, as of 03/02/2025*

![Market Regime Sample](Images/HurstExponentSample.png)

## Market Profile & Volume Profit Insights

- **Objective**: Analyze how price interacted with volume and liquidity to determine key market levels.
- **Methodology**:
  - Market Profile: Segments price action into price buckets to analyze how frequently each price level was traded.
    - Point of Control (PoC) - price level which saw the highest frequency of trading activity.
    - Value Area - the price range where 70% of trading activity occured, providing insight into what the market perceived as "fair value".
  - Volume Profile: Analyses how much volume was traded at each price level to determine liquidity zones.
    - Point of Control (PoC) - the price level with the highest traded volume
    - Value Area - the price range containing 70% of total traded volume.
  - **Application**
    - Market Profile helps speculators understand price acceptance and rejection zones.
    - Volume Profile highlights key liquidity areas where large institutional players might be active.  

**Sample Output**:
*Market Profile for Crude Oil as of 03/02/2025*

![Market Profile Sample](Images/MarketProfileSample.png)

![Volume Profile Sample](Images/VolumeProfileSample.png)
