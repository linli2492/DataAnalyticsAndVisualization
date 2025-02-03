# Quantitative Analysis on Futures

**Enhancing Trading Decisions Through Data-Driven Market Insights**

This project provides a versatile set of quantitative tools for analyzing futures price and volume data, offering a structured approach to volatility analysis, regime detection, and market structure evaluation. While this repository focuses on Crude Oil, the methodologies and tools can be applied to any asset class, including equities, FX, commodities, and fixed income.

By leveraging statistical techniques and financial market models, this framework helps traders:

- Contextualize price movements using volatility distributions and historical comparisons.
- Identify market regimes using Hurst exponent analysis to differentiate between trending vs. mean-reverting conditions, helping traders select the appropriate strategy.
- Analyze market structure via Market Profile and Volume Profile to highlight key price levels, liquidity zones, and fair value areas.

This repository serves as a quantitatively driven research framework, equipping traders with actionable insights for any instrument they wish to trade.

## Key Components

**Volatility Analysis**

- **Objective**: Compare the most recent trading session's volatility against historical distributions over 1-month, 3-month, 6-month, and 12-month timeframes.
- **Methodology**:
  - Compute daily high-low range distributions.
  - Uses Kernel Density Estimation (KDE) & histograms to visualize how the latest volatility compares to historical averages.
- **Sample Output**:
*Daily Volatility of Crude Oil as of 03/02/2025*

![Daily Volatility Sample](Images/DailyVolSample.png)

**Market Regime Detection**

Applies the **Hurst Exponent** to assess recent market behavior, distinguishing between mean-reverting and trending periods to guide traders to use the appropriate strategies. 

![Market Regime Sample](Images/HurstExponentSample.png)

**Market Profile & Volume Profit Insights**

Analyzes key **price levels, Points of Control (PoC) and Value Areas** to determine what the market perceived as *fair value* in prior trading sessions. 

Through these quantitative methods, the porject delivers **actionable insights** into any tradeable instrument that supports speculators in making **data-backed decisions** that align with current market dynamics. 

![Market Profile Sample](Images/MarketProfileSample.png)

![Volume Profile Sample](Images/VolumeProfileSample.png)
