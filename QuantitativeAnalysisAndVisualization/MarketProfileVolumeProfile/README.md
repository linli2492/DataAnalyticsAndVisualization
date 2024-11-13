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

This project builds a **Market Profile** and **Volume Profile** to pinpoint areas of fair value and highlight potential trading opportunities by aggregating an asset's price data and analyzing it's distrubution based on volume and time. 

By identifying where price activity clusters, traders can gain insight into: 
- **Fair Value**: Prive levels that have seen the most volume and time, representing areas of market agreement.  
- **Areas of Imbalance**: Low-activity zones that may present long or short opportunities if price re-enters these areas. 
- **Market Sentiment**: Levels that consistently attract or repel trading activity, revealing partiticpant confidence or hesitation. 

## Volume Profile

The Volume Profile highlights price levels where most trading volume occurred, helping to pinpoint fair value zones based on where market participants are most active.

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

**Limitations**: Volume Profile alone lacks context about market sentiment and participant behavior. Volume data alone does not reveal how long prices stayed in certain areas or the sequence of price movements, which are crucial to understanding whether the market accepts or rejects certain price levels.

## Market Profile

While the Volume Profile aggregates price data by volume, the Market Profile segments trading sessions into time-based intervals, typically 30-minute periods represented by letters. Market Profile thus adds a time element to volume data, giving traders a richer understanding of how price levels develop and change over a session.

Each coloured box with a letter represents a 30 minute interval of data, starting at ['A']. So ['A'] in [**this example**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPO.png), represents all the prices hit between 00:00 to 00:30 (in this case, 2668.4 to 2671.4) and ['B'] being 00:30 to 01:00 etc etc. 

**Key Insights from Market Profile:**
- **Trading Activity Over Time:** Market Profile shows not only price levels with high activity but also how price moves over time within a session, highlighting whether participants accept or reject certain prices.
- **Enhanced Value Area Identification:** Market Profile can validate value areas identified in the Volume Profile by confirming whether the market spent significant time at these levels.
- **Structural Integrity of Price Levels:** Market Profile offers structural insights that reveal the strength or weakness of highs and lows. For example:
  - **Strong Highs/Lows:** Represented by single prints, indicating sharp reversals with limited trading activity at the extremes. A strong high or low suggests a firm rejection by the market, often marking a boundary where buyers or sellers stepped in forcefully. In the [**Market Profile for GC 12-24 on November 11th**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPO.png), we see single prints from 'C' at 2650.3 to 2652.7 and from 'AO' at 2716.3 to 2718.2, indicating firm rejection of these price levels.
  - **Poor Highs/Lows**:Indicated by multiple prints at the extremes, showing that price lingered at these levels without making a decisive move. Poor highs or lows signal a lack of conviction from market participants, leaving these levels vulnerable to retests or breakouts. In the [**Market Profile for CL 11-24 (Light Crude Futures expiring November) on October 14th**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPOCL11-24.png), we can see an example of a Poor High where there are multiple prints at 74.83 and 74.82 REPHRASE IF NECESSARY, ALSO ADDING WHAT IT SUGGESTS
  - **Weak Highs/Lows**: Weak highs or lows can sometimes appear at technical levels (e.g., previous day’s high, a round number). They can exhibit single prints, but they are often driven by technical levels rather than by strong fundamental interest, making them susceptible to retests.

A Market Profile can also be visualized as a bar chart *as per the below*, providing a compact summary of trading activity. This format allows traders to quickly view key information without extensive scrolling, which is particularly helpful when the price range is broad and multiple price levels need to be represented efficiently
<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfile.png" alt="Market Profile Graph">
</p>

## Summary of Findings on GC 12-24

When used together, Market and Volume Profiles provide a comprehensive view of market activity:
- **Volume Profile identifies key value areas**, but Market Profile adds depth by revealing the time component and the structural integrity of price levels.
- **Market Profile can clarify whether high-volume nodes represent fair value** by showing whether the market spent significant time there.
- **Areas of Imbalance**: Market Profile helps identify structural weak points like poor or weak highs/lows, which could offer reversal or breakout opportunities.

From the above information traders can deduce the following and implement the following trading strategy for 8th November, as an example: 
- Fair value moved from c2660-2674 to 2696-2708 as confirmed by both Volume Profile and Market Profile distributions.
  - Gold had rebounded from Wednesday's sell-off following Donald Trump's definitive victory over Kamala Harris. Gold had seen extended bets from traders in the run-up to the election. Therefore, Trump's victory was likely to be the catalyst for investors to unwind safe-haven Gold positions.
- Single prints were observed at the Highs and Lows of the day providing it a Strong High and Low.
- No significant economic releases scheduled for November 8th that would significantly impact Gold.

Traders can implement a Mean-Reverting strategy/algorithm that:
- **Places a Long trade** should price move below 2696 absent of any fundamental news releases and indicators such as the RSI indicate overselling and ADX indicate a lack of momentum in price action.
- **Places a Short trade** should price move above 2708 absent of any fundamental news releases and indicators such as the RSI indicate overbuying and ADX indicate a lack of momentum in price action.

