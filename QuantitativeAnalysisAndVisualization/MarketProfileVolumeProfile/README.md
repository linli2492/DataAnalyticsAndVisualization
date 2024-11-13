# Ascertaining the Fair Value of an Asset Using Market Profile and Volume Profile Distribution Curves

**Disclaimer: This content is provided solely for educational purposes and should not be considered as financial or investment advice. The information presented is intended to enhance understanding of financial concepts and trading methodologies. Always consult with a qualified financial advisor before making any investment decisions.**

## Table of Content
- [Project Overview](#project-overview)
- [Volume Profile](#volume-profile)
- [Market Profile](#market-profile)
- [Summary of Findings on GC 12-24](#summary-of-findings-on-gc-12-24)

## Project Overview
Traders who use Auction Market Theory aim to identify the fair value of an asset and seek trading opportunities by analyzing imbalances in supply and demand dynamics.

Typically, traders will:
- **Fade "unfair" prices** when there is insufficient conviction at a given value, expecting reversion towards a fair value area.
- **Trade in the direction of "unfair" prices** if there is sufficient momentum, indicating a potential shift to a new value area.

This project builds a **Market Profile** and **Volume Profile** to pinpoint areas of fair value and highlight potential trading opportunities by aggregating an asset's price data and analyzing its distribution based on volume and time. 

By identifying where price activity clusters, traders can gain insight into: 
- **Fair Value**: Price levels that have seen the most volume and time, indicating areas where the market agrees on price.  
- **Areas of Imbalance**: Low-activity zones that may present long or short opportunities if price re-enters these areas. 
- **Market Sentiment**: Levels that consistently attract or repel trading activity, revealing participant confidence or hesitation. 

## Volume Profile

The Volume Profile highlights price levels with the highest trading volume, helping pinpoint fair value zones based on active trading levels

The below is a Volume Profile of GC 12-24 (Gold Futures expiring on December 2024) on the 7th November 2024. 

Example: Below is a Volume Profile of GC 12-24 (Gold Futures expiring on December 2024) on November 7, 2024. It was created by aggregating total volume transacted at each price level throughout the trading day, creating a distribution that shows the price levels with the most trading activity.

<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/VolumeProfile.png" alt="Volume Profile Graph">
</p>

From the above a trader can ascertain the following: 

- **Fair Value**: This is typically represented by high-volume nodes where the price spent the most time and attracted the most volume. On November 7, fair value zones identified were between 2660-2674 and 2694-2708.
    
- **Trending Day**: A bimodal or multimodal distribution can signify a trending day. Multiple volume peaks may indicate distinct areas of value, often marking shifts in market perception. Volume Profile alone does not indicate trend direction, but by comparing with a candlestick chart, we can confirm that GC 12-24 on November 7 trended upwards (*see below*).
  
- **Areas of Imbalance**: Zones with relatively low trading volume reflect price levels where the market moved quickly, often signifying inefficiencies or imbalances. When price re-enters these zones, they may offer trading opportunities, either as continuation or reversal points depending on market context.

<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/Candlestick.png" alt="Candlestick Graph">
</p>

**Limitations**: Volume Profile alone lacks context about market sentiment and participant behavior. Volume data by itself does not reveal how long prices remained at certain levels or the order of price movements, both of which are crucial for understanding whether the market is accepting or rejecting specific price levels.

## Market Profile

While the Volume Profile aggregates price data by volume, the Market Profile segments trading sessions into time-based intervals, typically 30-minute periods represented by letters. Market Profile thus adds a time element to volume data, giving traders a richer understanding of how price levels develop and change over a session.

Each coloured box with a letter represents a 30 minute interval of data, starting at ['A']. So ['A'] in [**this example**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPO.png), represents all the prices hit between 00:00 to 00:30 (in this case, 2668.4 to 2671.4) and ['B'] being 00:30 to 01:00 etc etc. 

**Key Insights from Market Profile:**
- **Trading Activity Over Time:** Market Profile shows not only price levels with high activity but also how price moves over time within a session, highlighting whether participants accept or reject certain prices.
- **Enhanced Value Area Identification:** Market Profile can validate value areas identified in the Volume Profile by confirming whether the market spent significant time at these levels.
- **Structural Integrity of Price Levels:** Market Profile offers structural insights that reveal the strength or weakness of highs and lows. For example:
  - **Strong Highs/Lows:** Represented by single prints, indicating sharp reversals with limited trading activity at the extremes. A strong high or low suggests a firm rejection by the market, often marking a boundary where buyers or sellers stepped in forcefully. In the [**Market Profile for GC 12-24 on November 11th**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPO.png), we see single prints from 'C' at 2650.3 to 2652.7 and from 'AO' at 2716.3 to 2718.2, indicating firm rejection of these price levels.
  - **Poor Highs/Lows**: Indicated by multiple letters or trading intervals at the extreme highs or lows, showing that price lingered at these levels without making a decisive move. Poor highs or lows signal a lack of conviction from market participants, leaving these levels vulnerable to retests or potential breakouts. In the [**Market Profile for CL 11-24 (Light Crude Futures expiring November) on October 14th**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPOCL11-24.png), the Poor High has multiple prints at 74.83 and 74.82, suggesting possible retests in the future.
  - **Weak Highs/Lows**: Weak highs or lows are often triggered by technical levels, such as a previous day’s high, a round number, or a prior low. While they can exhibit single prints, these levels are frequently driven by technical triggers like stop orders rather than fundamental buying or selling interest, making them susceptible to retests.

A Market Profile can also be visualized as a bar chart, providing a compact summary of trading activity. This format allows traders to quickly view key information without extensive scrolling, which is particularly helpful when the price range is broad, and multiple price levels need to be represented efficiently. [*see below*]

<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfile.png" alt="Market Profile Graph">
</p>

## Summary of Findings on GC 12-24

When used together, Market and Volume Profiles provide a comprehensive view of market activity:
- **Volume Profile identifies key value areas**, but lacks the time and structural insights provided by the Market Profile.
- **Market Profile clarifies whether high-volume nodes represent fair value** by showing if the market spent significant time at those levels.
- **Identifying Imbalance**: Market Profile reveals structural weak points like poor or weak highs/lows, which may indicate reversal or breakout potential.

From the above information, traders can deduce the following: 
- **Fair Value Shift**: Fair value shifted from 2660-2674 to 2696-2708, confirmed by both the Volume Profile and Market Profile distributions
  - **Market Context**: Gold rebounded following Wednesday’s sell-off after Donald Trump's definitive victory over Kamala Harris, triggering a liquidation of safe-haven positions. This political outcome was likely the catalyst for traders to unwind extended bets on gold.
- **Structural Levels**: Single prints observed at the Highs and Lows of the day indicate a Strong High and Strong Low.
- No significant economic releases were scheduled for November 8th to impact gold.

Traders can implement a Mean-Reverting strategy/algorithm on November 8th that:
- **Places a Long trade** should price move below 2696, absent of any fundamental news releases, and with indicators such as RSI indicating overselling and ADX indicating a lack of momentum in price action.
- **Places a Short trade** should price move above 2708, absent of any fundamental news releases, and with indicators such as RSI indicating overbuying and ADX indicating a lack of momentum in price action.

