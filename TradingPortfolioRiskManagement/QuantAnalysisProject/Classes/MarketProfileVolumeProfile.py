import pandas as pd
import numpy as np
import math
import string
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class MarketProfileVolumeProfile:
    """
    A class to calculate and visualize Market Profile, Volume Profile, and Market Profile with Letters
    for price, volume, and letter-mapping data.

    This class provides tools for building and visualizing market and volume profiles:
    - Market Profile: Aggregates data into price levels, identifies high-activity price zones, and calculates key levels such as 
      the Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL) based on market dynamics.
    - Volume Profile: Aggregates trade volume at each price level, helping visualize where most of the trading volume occurred, 
      with PoC, VAH, and VAL calculations.
    - Market Profile with Letters: Maps letters to price levels to represent individual time periods within each price level, 
      helping identify patterns and high-activity zones by visually encoding price movement.

    Parameters:
    - granularity: Defines the price level interval for each profile (e.g., 0.01, 0.05). Smaller values create finer profiles, 
      while larger values result in more aggregated profiles.

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
        
    def market_profile_and_visualize_letters(self, df, granularity, show_visualization=True):
        """
        Aggregates the data into price buckets based on the provided granularity, uses letters 
        to represent time intervals within a trading session, and appends these letters to each 
        price bucket that falls between the High and Low of each interval.

        This method creates a "Market Profile with Letters" by associating each price bucket with 
        a specific letter, allowing users to observe market structure visually across time intervals. 
        The visual representation uses letters to encode time-based price movement, helping to identify 
        recurring patterns or high-activity zones.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing price data with OHLC (Open, High, Low, Close) columns.
        granularity : float
            The granularity for price buckets (e.g., 0.001, 0.005, 0.01, etc.). Smaller values 
            offer finer segmentation of prices, while larger values create broader price buckets.
        show_visualization : bool, optional
            If True, displays a visualization of the Market Profile with Letters (default is True).

        Returns
        -------
        dict
            A dictionary where each key is a price level and the value is a list of letters 
            representing time intervals (rows) that include that price within their High-Low range.

        tuple
            Additional key price levels including Point of Control (PoC), Value Area High (VAH), 
            and Value Area Low (VAL).

        Raises
        ------
        ValueError
            If the granularity is not positive or not within the accepted range.
        KeyError
            If the required columns ('Open', 'High', 'Low', 'Close') are missing from the DataFrame.
        Exception
            For any other unexpected error.
        """

        try:
            # Validate granularity
            if not isinstance(granularity, (float, int)) or granularity <= 0:
                raise ValueError("Granularity must be a positive number.")

            # Check required columns
            required_columns = {'Open', 'High', 'Low', 'Close'}
            if not required_columns.issubset(df.columns):
                raise KeyError(f"DataFrame must contain the following columns: {required_columns}")

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

            # Calculate counts for each price level
            price_counts = {price: len(letters) for price, letters in price_dict.items()}

            # Sort price levels in descending order
            sorted_price_counts = dict(sorted(price_counts.items(), reverse=True))

            # Calculate PoC, Value Area High (VAH) and Value Area Low (VAL)
            total_count = sum(sorted_price_counts.values())
            value_area_threshold = total_count * 0.7
            poc = max(sorted_price_counts, key=sorted_price_counts.get)

            cumulative_count = 0
            value_area_prices = []
            for price, count in sorted_price_counts.items():
                cumulative_count += count
                value_area_prices.append(price)
                if cumulative_count >= value_area_threshold:
                    break

            vah = max(value_area_prices)
            val = min(value_area_prices)

            # Visualization block
            if show_visualization:
                unique_letters = sorted(set(letter for letters in return_dict.values() for letter in letters))
                letter_colors = {letter: plt.cm.tab20(random.randint(0, 19)) for letter in unique_letters}

                # Prepare data for plotting
                price_levels = list(return_dict.keys())
                max_letters = max(len(letters) for letters in return_dict.values())  # Max number of letters in any price bucket

                # Create a smaller figure with a compact grid layout
                fig, ax = plt.subplots(figsize=(6, len(price_levels) * 0.15))

                # Plot each letter in its own colored box
                for y_index, price in enumerate(reversed(price_levels)):  # Highest price at top
                    letters = return_dict[price]

                    for x_index, letter in enumerate(letters):
                        # Define a smaller rectangle for each letter
                        rect = patches.Rectangle((x_index, y_index), 0.8, 0.8, linewidth=0.5,
                                                 edgecolor='black', facecolor=letter_colors[letter])
                        ax.add_patch(rect)
                        # Add text of the letter inside the rectangle with a smaller font
                        ax.text(x_index + 0.4, y_index + 0.4, letter, ha='center', va='center', fontsize=6, color="black")

                # Set axis labels and title
                ax.set_yticks(range(len(price_levels)))
                ax.set_yticklabels(reversed(price_levels), fontsize=6)
                ax.set_xticks([])  # Remove x-axis ticks
                ax.set_xlabel("Occurrences", fontsize=8)
                ax.set_ylabel("Price Levels", fontsize=8)
                ax.set_title(f"Market Profile TPO Visualization of {self.futures_name} on {self.date}", fontsize=10)

                # Set limits and display
                ax.set_xlim(0, max_letters)
                ax.set_ylim(-0.5, len(price_levels) - 0.5)
                ax.invert_yaxis()
                plt.show() 

            # Return dictionary with reversed order (descending by price)
            return {k: return_dict[k] for k in reversed(return_dict)}, poc, vah, val

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None, None, None, None

        except KeyError as ke:
            print(f"KeyError: {ke}")
            return None, None, None, None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None, None, None

    def market_profile_and_visualize_bars(self, df, granularity, show_visualization=False):
        """
        Aggregates the data into price buckets based on the provided granularity,
        calculates the Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL),
        and optionally visualizes the data.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing price data with OHLC columns ('Open', 'High', 'Low', 'Close').
        granularity : float
            The granularity for price buckets, used to segment prices.
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
            If the granularity is not positive or outside the accepted range.
        KeyError
            If required columns ('Open', 'High', 'Low', 'Close') are missing from the DataFrame.
        Exception
            For any unexpected errors.
        """
        try:
            #Validate granularity input
            if not isinstance(granularity, (float, int)) or granularity <= 0:
                raise ValueError("Granularity must be a positive number.")
            # Validate the granularity input
            if granularity not in [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25]:
                raise ValueError("Granularity must be one of 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, or 0.25")
            
            # Check required columns
            required_columns = {'Open', 'High', 'Low', 'Close'}
            if not required_columns.issubset(df.columns):
                raise KeyError(f"DataFrame must contain the following columns: {required_columns}")

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
                    title=f"Market Profile Bar Chart of {self.futures_name} on {self.date}",
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
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None, None, None, None

        except KeyError as ke:
            print(f"KeyError: {ke}")
            return None, None, None, None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None, None, None

    def volume_profile_and_visualize(self, df, granularity, show_visualization=False):
        """
        Aggregates the data into volume buckets based on the provided granularity,
        calculates the Point of Control (PoC), Value Area High (VAH), and Value Area Low (VAL),
        and optionally visualizes the data.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing price and volume data with OHLC and Volume columns ('Open', 'High', 'Low', 'Close', 'Volume').
        granularity : float
            The granularity for price buckets, used to segment prices.
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
            If granularity is not positive or is outside the accepted range.
        KeyError
            If required columns ('Open', 'High', 'Low', 'Close', 'Volume') are missing from the DataFrame.
        Exception
            For any unexpected errors.
        """
        try:
            # Validate granularity
            if not isinstance(granularity, (float, int)) or granularity <= 0:
                raise ValueError("Granularity must be a positive number.")
            if granularity not in [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.25]:
                raise ValueError("Granularity must be one of 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, or 0.25")
        
            # Check for required columns
            required_columns = {'Open', 'High', 'Low', 'Close', 'Volume'}
            if not required_columns.issubset(df.columns):
                raise KeyError(f"DataFrame must contain the following columns: {required_columns}")

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
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None, None, None, None

        except KeyError as ke:
            print(f"KeyError: {ke}")
            return None, None, None, None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None, None, None
    
    def price_structure_analysis(self, agg_dict):
        """
        Analyzes the price structure of a given Market Profile or Volume Profile distribution to determine 
        the strength or weakness of high and low price levels, identifying potential Poor/Weak Highs and Lows.

        This analysis identifies structural characteristics by assessing the frequency of occurrences (letter 
        or volume counts) at the extreme high and low price levels in the profile. It is particularly useful 
        for detecting areas where the market may have left behind imbalances, indicating levels that could 
        attract future price action.

        Parameters
        ----------
        agg_dict : dict
            A dictionary where keys represent price levels and values represent the list of letters, volume, 
            or counts associated with each price level.

        Returns
        -------
        None

        Prints
        ------
        A description of the high and low price structures:
            - "Poor/Weak High": Printed if the high price level shows significant activity, which may indicate 
              a lack of strong conviction from sellers, leaving the high susceptible to retesting.
            - "Strong High": Printed if there is minimal activity at the high price level, suggesting that 
              sellers strongly rejected higher prices.
            - "Poor/Weak Low": Printed if the low price level shows significant activity, which may indicate 
              a lack of strong conviction from buyers, leaving the low susceptible to retesting.
            - "Strong Low": Printed if there is minimal activity at the low price level, suggesting that buyers 
              strongly rejected lower prices.

        Raises
        ------
        ValueError
            If agg_dict is not a dictionary or if it does not contain enough price levels to analyze.
        TypeError
            If values in agg_dict are not in a compatible format (e.g., list, tuple, or string).
        Exception
            For any other unexpected errors.
        """  
        try:
            # Validate agg_dict type and structure
            if not isinstance(agg_dict, dict):
                raise ValueError("agg_dict must be a dictionary with price levels as keys.")

            if len(agg_dict) < 2:
                raise ValueError("agg_dict must contain at least two price levels to perform analysis.")

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
                
        except ValueError as ve:
            print(f"ValueError: {ve}")

        except TypeError as te:
            print(f"TypeError: {te} - Ensure all values in agg_dict are list, tuple, or str types.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
