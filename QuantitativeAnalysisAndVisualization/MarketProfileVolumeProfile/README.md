# Ascertaining the Fair Value of an Asset Using Market Profile and Volume Profile Distribution Curves

## Table of Content
- [Project Overview](#project-overview)
- [Volume Profile](#volume-profile)
- [Market Profile](#market-profile)

## Project Overview
Traders that use Auction Market Theory will first identify the fair value of an asset and seek trading opportunities by identifying imbalances in the supply and demand dynamics.

Typically, traders will: 
- Fade 'unfair' prices when they sense insufficient conviction in the current value, expecting a reversion towards a fair value area. 
- Trade in the direction of unfair prices when there is sufficient momentum, signaling a potential shift to a new value area.

This project builds a **Market Profile** and **Volume Profile** to pinpoint areas of value and trading opportunities by aggregating an asset's price data and analyzing it's distrubution viewed in terms of volume and time.

By analysing where price activity clusters, traders can gain insight into: 
- **Fair Value**: Typically at price levels that has seen the most volume and the most time spent. 
- **Areas of Imbalance**: Low-activty zones that may present long or short opportunities if price re-enters these areas.
- **Market Sentiment**: Levels that consistently attract or repel trading activity, revealing partiticpant sentiment and confidence in those areas.

## Volume Profile

Volume Profiles highlight price levels where the most trading volumed occured, helping pinpoint fair value zones based on where market participants are most actively trading.

The below is a Volume Profile of GC 12-24 (Gold Futures expiring on December 2024) on the 7th November 2024. 

This profile was constructed by aggregating the total volume transacted at each price level through the trading day, creating a distribution that highlights the price levels where the most trading activity occured. 

<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/VolumeProfile.png" alt="Volume Profile Graph">
</p>

From the above a trader can ascertain the following: 

- **Fair Value**: This is typically represented by the high-volume nodes in the distribution where the price spent the most time and attracted the most volume. Fair value zones identified on the 7th November are between 2660-2674 and 2694-2708.
    
- **Trending Day**: A trending day is often identified by a *bimodal* or even *multimodal* distribution. In such cases, two or more peaks in trading volume suggest distinct areas of value, often marking shifts in perception during the session. Though the Volume Profile alone cannot give us the direction of the trend, looking at a candlestick chart can. GC 12-24 on the 7th November trended upwards (*see below*).
  
- **Areas of Imbalance**: These zones with relatively low trading volume signify price levels where the market moved quickly through, often indicating ineffiencies or imbalances. When price re-enters these zones, they may offer potential opportunities to trade in the direction of the trend or for a reversal, depending on market context.

<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/Candlestick.png" alt="Candlestick Graph">
</p>

Though Volume Profile offers insights into trading activity, alone, it lacks context on market sentiment and participant behavior. 

Volume data alone does not reveal how long prices remained in a particular area or the sequence of price movements, which are crucial for understanding whether the market is accepting or rejecting certain price levels. 


## Market Profile

Whilst Volume Profile distributions aggregates price data by volume, Market Profile distributions segments a trading session into time-based intervals, typically 30 minutes each, represented by letters. 

A Market Profile enables traders to visualize not only price levels with the highest activity, but also how price moves over time within a session. 

Through a Market Profile, traders can infer whether participants are accepting or rejecting prices, highlighting key levels that may represent support, resistance or potential for reversion.

[**The Market Profile for GC 12-24 (Gold Futures expiring December 2024) on November 11 shows the distribution across the full trading day, starting from 00:00**](https://github.com/linli2492/ProjectsPortfolio/tree/main/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfileTPO.png)

Each coloured box with a letter represents a 30 minute interval of data, starting at ['A']. So ['A'] in the example above, represents all the prices hit between 00:00 to 00:30 (in this case, 2668.4 to 2671.4) and ['B'] being 00:30 to 01:00 etc etc. 

A Market Profile provides structure to volume data by mapping where price spent the most time and can indicate the following: 
- 



<p align="center">
  <img src="/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfile.png" alt="Market Profile Graph">
</p>



## Auction Market Theory Summarised


For a more in depth discussion on Auction Market Theory, please refer to the AuctionMarketTheory.md file as this is beyond the scope of this README. 
