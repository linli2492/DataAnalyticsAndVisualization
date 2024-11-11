# Ascertaining the Fair Value of an Asset Using Market Profile and Volume Profile Distribution Curves

## Table of Content
- [Project Overview](#project-overview)
- [Volume Profile](#volume-profile)
- [Market Profile](#market-profile)

## Project Overview
Traders use Auction Market Theory seek trading opportunities by analyzing imbalances in supply and demand for an asset. 

This project leverages Market Profile and Volume Profile distributions to help traders identify areas of value and potential trading setups based on these imbalances. 

Typically, traders will: 
- Fade 'unfair' prices when they sense insufficient conviction in the current value, expecting a reversion towards a fair value area. 
- Trade in the direction of unfair prices when there is sufficient momentum, signaling a potential shift to a new value area.

A fundamental step in both strategies is locating these "value areas" for the asset being traded.

## Project Purpose

This project builds a Market Profile and Volume Profile to pinoint areas of value and trading opportunities by aggregating price data and analyzing it's distrubution viewed in terms of volume and time

A pre-requisite to any of the above strategies is to find the areas of value of the asset you are trading.  

By analysing where price activity clusters, traders can gain insight into: 
- **Fair Value**: Price levels where there is the least contention between buyers and sellers.
- **Areas of Imbalance**: Low-activty zones that may present long or short opportunities if price re-enters these areas.
- **Market Sentiment**: Levels taht consistently attract or repel trading activity, revealing partiticpant sentiment and confidence in those areas. 

## Volume Profile

The below is a Volume Profile of GC 12-24 on on the 7th November 2024. 

This profile was constructed by aggregating the total volume transacted at each price level through the trading day, creating a distribution that highlights the price levels where the most trading activity occured. 

![Volume Profile Graph](/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/VolumeProfile.png)

Volume profiles aim to highlight areas of high and low volume, helping traders identify areas of balance and imbalance. 

## Market Profile

![Market Profile Graph](/QuantitativeAnalysisAndVisualization/MarketProfileVolumeProfile/images/MarketProfile.png)



## Auction Market Theory Summarised


For a more in depth discussion on Auction Market Theory, please refer to the AuctionMarketTheory.md file as this is beyond the scope of this README. 
