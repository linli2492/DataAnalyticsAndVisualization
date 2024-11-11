import pandas as pd
import numpy as np
import math
import string
import plotly.graph_objects as go

class MarketProfileVolumeProfile:
    """
    A class to calculate and visualize Market Profile, Volume Profile, and Market Profile with Letters
    for price, volume, and letter-mapping data.

    Methods
    -------
    generate_letter_list(n):
        Generates a list of letters for labeling rows in the Market Profile.

    market_profile_with_letters(df, granularity):
        Aggregates data into price buckets, represents rows with letters, and appends letters to each price bucket.

    market_profile_and_visualize(df, granularity, show_visualization=False):
        Aggregates data into price buckets and calculates Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL),
        with an option to visualize the distribution.

    volume_profile_and_visualize(df, granularity, show_visualization=False):
        Aggregates data into volume buckets and calculates PoC, VAH, VAL, with an option to visualize the distribution.
    """

    def __init__(self, futures_name, date):
        """
        Initializes the MarketProfileVolumeProfile class.
        """
        self.futures_name = futures_name
        self.date = date
        pass

    def generate_letter_list(self, n):
        """
        Generate a list of n letters starting from A-Z, followed by AA, AB, ..., AZ, BA, ..., ZZ, AAA, AAB, and so on.

        Parameters
        ----------
        n : int
            The number of letters to generate.

        Returns
        -------
        list
            A list of strings representing the sequence of letters.
        """
        letters = []
        alphabet = string.ascii_uppercase
        alphabet_length = len(alphabet)

        for i in range(n):
            letter = ""
            while i >= 0:
                # Calculate the remainder and update the letter string from right to left
                letter = alphabet[i % alphabet_length] + letter
                i = i // alphabet_length - 1
            letters.append(letter)

        return letters

    def market_profile_with_letters(self, df, granularity):
        """
        Aggregates the data into price buckets based on the provided granularity,
        uses letters to represent rows, and appends the letters to each price bucket
        that falls between the High and Low of each row.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing price data with OHLC (Open, High, Low, Close) columns.
        granularity : float
            The granularity for price buckets (e.g., 0.001, 0.005, 0.01, etc.).

        Returns
        -------
        dict
            A dictionary where each key is a price level and the value is a list of letters 
            representing rows that include that price in their High-Low range.

        Raises
        ------
        ValueError
            If the granularity provided is not one of the accepted values.
        """
        # Validate the granularity input
        if granularity not in [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25]:
            raise ValueError("Granularity must be one of 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, or 0.25")

        # Determine the lowest and highest prices in the data
        lowest_price = df[['Open', 'High', 'Low', 'Close']].min().min()
        highest_price = df[['Open', 'High', 'Low', 'Close']].max().max()

        # Calculate minimum and maximum prices rounded to two decimal places
        min_price = round(math.floor(lowest_price * 1000) / 1000, 3)
        max_price = round(math.ceil(highest_price * 1000) / 1000, 3)

        # Initialize a dictionary to store the letters for each price level
        price_dict = {round(price, 3): [] for price in np.arange(min_price, max_price, granularity)}

        # Generate a list of letters (for the number of rows in the dataframe)
        letters = self.generate_letter_list(len(df))

        # Append letters to price buckets based on the high and low prices in each row
        for idx, row in enumerate(df.iterrows()):
            letter = letters[idx]  # Get the letter corresponding to the row
            low = round(row[1]['Low'], 3)
            high = round(row[1]['High'], 3)
            for price in np.arange(low, high + granularity, granularity):
                price = round(price, 3)
                if price in price_dict:
                    price_dict[price].append(letter)  # Store only the letter

        # Sort the price buckets in descending order
        return_dict = {price: letters for price, letters in price_dict.items()}
        
        # Return dictionary with reversed order (descending by price)
        return {k: return_dict[k] for k in reversed(return_dict)}

    def market_profile_and_visualize(self, df, granularity, show_visualization=False):
        """
        Aggregates the data into price buckets based on the provided granularity,
        calculates the Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL),
        and optionally visualizes the data.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing price data with OHLC columns.
        granularity : float
            The granularity for price buckets.
        show_visualization : bool, optional
            If True, displays a chart of the Market Profile distribution (default is False).

        Returns
        -------
        tuple
            A tuple (dict, float, float, float), where:
            - dict: Aggregated counts of price occurrences,
            - float: Point of Control (PoC),
            - float: Value Area High (VAH),
            - float: Value Area Low (VAL).

        Raises
        ------
        ValueError
            If the granularity provided is not one of the accepted values.
        """
        # Validate the granularity input
        if granularity not in [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25]:
            raise ValueError("Granularity must be one of 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, or 0.25")

        # Determine the lowest and highest prices in the data
        lowest_price = df[['Open', 'High', 'Low', 'Close']].min().min()
        highest_price = df[['Open', 'High', 'Low', 'Close']].max().max()

        # Calculate minimum and maximum prices rounded to three decimal places
        min_price = round(math.floor(lowest_price * 1000) / 1000, 3)
        max_price = round(math.ceil(highest_price * 1000) / 1000, 3)

        # Initialize a dictionary to count occurrences at each price level
        price_dict = {round(price, 3): 0 for price in np.arange(min_price, max_price, 0.001)}

        # Count the number of times each price level occurs based on high and low prices
        for _, row in df.iterrows():
            low = round(row['Low'], 3)
            high = round(row['High'], 3)
            for price in np.arange(low, high, granularity):
                price = round(price, 3)
                if price in price_dict:
                    price_dict[price] += 1

        # Aggregate the counts for the specified granularity
        aggregated_dict = {}
        multiplier = int(1 / granularity)
        for price in price_dict:
            bucket = round(math.floor(price * multiplier) / multiplier, 3)
            if bucket not in aggregated_dict:
                aggregated_dict[bucket] = 0
            aggregated_dict[bucket] += price_dict[price]
            
        sorted_aggregated_dict = dict(sorted(aggregated_dict.items(), reverse=True))

        # Sort the price buckets for visualization
        prices, counts = zip(*sorted_aggregated_dict.items())

        # Calculate Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL)
        total_count = sum(counts)
        value_area_threshold = total_count * 0.70
        poc_index = np.argmax(counts)
        poc = prices[poc_index]

        cumulative_count = 0
        value_area_prices = []
        for i in np.argsort(counts)[::-1]:
            cumulative_count += counts[i]
            value_area_prices.append(prices[i])
            if cumulative_count >= value_area_threshold:
                break

        vah = max(value_area_prices)
        val = min(value_area_prices)

        # Visualize the Market Profile if requested
        if show_visualization:
            fig = go.Figure(go.Bar(
                x=counts,
                y=prices,
                orientation='h',
                marker=dict(color=counts, colorscale='Viridis', showscale=True),
            ))
            fig.update_layout(
                title=f"Market Profile of {self.futures_name} on {self.date}",
                xaxis_title="Count",
                yaxis_title="Price",
                yaxis=dict(tickmode='linear', dtick= 20 * granularity),
                xaxis=dict(tickmode='linear', dtick=max(counts) // 10 or 1),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color='black'),
                height=600,
            )
            fig.show()

        return sorted_aggregated_dict, poc, vah, val

    def volume_profile_and_visualize(self, df, granularity, show_visualization=False):
        """
        Aggregates the data into volume buckets based on the provided granularity,
        calculates the Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL),
        and optionally visualizes the data.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing price and volume data with OHLC and Volume columns.
        granularity : float
            The granularity for price buckets.
        show_visualization : bool, optional
            If True, displays a chart of the Volume Profile distribution (default is False).

        Returns
        -------
        tuple
            A tuple (dict, float, float, float), where:
            - dict: Aggregated volumes at each price level,
            - float: Point of Control (PoC),
            - float: Value Area High (VAH),
            - float: Value Area Low (VAL).

        Raises
        ------
        ValueError
            If the granularity provided is not one of the accepted values.
        """
        # Validate the granularity input
        if granularity not in [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25]:
            raise ValueError("Granularity must be one of 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, or 0.25")

        # Determine the lowest and highest prices in the data
        lowest_price = df[['Open', 'High', 'Low', 'Close']].min().min()
        highest_price = df[['Open', 'High', 'Low', 'Close']].max().max()

        # Calculate minimum and maximum prices rounded to three decimal places
        min_price = round(math.floor(lowest_price * 1000) / 1000, 3)
        max_price = round(math.ceil(highest_price * 1000) / 1000, 3)

        # Initialize a dictionary to store volume at each price level
        volume_dict = {round(price, 3): 0 for price in np.arange(min_price, max_price, granularity)}

        # Distribute volume across price levels based on high and low prices
        for _, row in df.iterrows():
            low = round(row['Low'], 3)
            high = round(row['High'], 3)
            volume = row['Volume']
            num_levels = len(np.arange(low, high, granularity))
            volume_per_level = volume / num_levels if num_levels > 0 else 0
            for price in np.arange(low, high, granularity):
                price = round(price, 3)
                if price in volume_dict:
                    volume_dict[price] += volume_per_level

        # Aggregate the volumes for the specified granularity
        aggregated_dict = {}
        multiplier = int(1 / granularity)
        for price in volume_dict:
            bucket = round(math.floor(price * multiplier) / multiplier, 3)
            if bucket not in aggregated_dict:
                aggregated_dict[bucket] = 0
            aggregated_dict[bucket] += volume_dict[price]
            
        sorted_aggregated_dict = dict(sorted(aggregated_dict.items(), reverse=True))

        # Sort the volume buckets for visualization
        prices, volumes = zip(*sorted_aggregated_dict.items())

        # Calculate Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL)
        total_volume = sum(volumes)
        value_area_threshold = total_volume * 0.70
        poc_index = np.argmax(volumes)
        poc = prices[poc_index]

        cumulative_volume = 0
        value_area_prices = []
        for i in np.argsort(volumes)[::-1]:
            cumulative_volume += volumes[i]
            value_area_prices.append(prices[i])
            if cumulative_volume >= value_area_threshold:
                break

        vah = max(value_area_prices)
        val = min(value_area_prices)

        # Visualize the Volume Profile if requested
        if show_visualization:
            fig = go.Figure(go.Bar(
                x=volumes,
                y=prices,
                orientation='h',
                marker=dict(color=volumes, colorscale='Viridis', showscale=True),
            ))
            fig.update_layout(
                title=f"Volume Profile of {self.futures_name} on {self.date}",
                xaxis_title="Volume",
                yaxis_title="Price",
                yaxis=dict(tickmode='linear', dtick=20 * granularity),
                xaxis=dict(tickmode='linear', dtick=max(volumes) // 10 or 1),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color='black'),
                height=600,
            )
            fig.show()

        return sorted_aggregated_dict, poc, vah, val
    
    def price_structure_analysis(self, agg_dict):
        keys = list(agg_dict.keys())

        # Select first two and remaining keys
        high_prices = keys[:2]
        low_prices = keys[-2:]

        # Sum lengths with additional debugging info for accuracy
        high_price_count = sum(
            len(agg_dict[key]) if isinstance(agg_dict[key], (list, tuple, str)) else 1 
            for key in high_prices
        )
        low_price_count = sum(
            len(agg_dict[key]) if isinstance(agg_dict[key], (list, tuple, str)) else 1 
            for key in low_prices
        )
        
        # Print statements for price structure
        
        if high_price_count > 2:
            print("Poor/Weak High")
        else:
            print("Strong High")

        if low_price_count > 2:
            print("Poor Weak Low")
        else:
            print("Strong Low")
