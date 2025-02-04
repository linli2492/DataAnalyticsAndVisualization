#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats
from plotly.subplots import make_subplots

class DailyVolatilityVisualiser:
    """
    A class for visualizing daily volatility profiles using interactive histograms and KDE.
    """
    
    def __init__(self, df):
        """
        Initializes the DailyVolatilityVisualiser with a DataFrame.

        Parameters:
        - df: Pandas DataFrame containing daily range data.
        """
        self.df = df
        self.df_last_20_days = df.head(20)['Range']  # 1 month data
        self.df_last_60_days = df.head(60)['Range']  # 3 month data
        self.df_last_120_days = df.head(120)['Range']  # 6 month data
        self.df_last_240_days = df.head(240)['Range']  # 12 month data
        self.latest_range = df['Range'].iloc[0]  # Latest day's range

    def interactive_histogram(self, historical_series, latest_data, bins, title, row, col, fig):
        """
        Creates an interactive histogram with KDE and a red vertical line for latest data.

        Parameters:
        - historical_series: The historical data series for the histogram.
        - latest_data: The latest range value to mark with a red vertical line.
        - bins: Number of bins for the histogram.
        - title: The title for the subplot.
        - row, col: The subplot position in the grid.
        - fig: The Plotly figure to which the subplot will be added.
        """
        # Histogram with frequencies (Counts) & Outlined Bars
        fig.add_trace(go.Histogram(
            x=historical_series,
            xbins=dict(size=(max(historical_series) - min(historical_series)) / bins),  # Bin size calculation
            marker=dict(
                color="blue", 
                opacity=0.6, 
                line=dict(width=1, color="black")  # Adds black lines separating bars
            ),
            name=f"{title} Histogram"
        ), row=row, col=col)

        # KDE (Kernel Density Estimate)
        kde_x = np.linspace(min(historical_series), max(historical_series), 100)
        kde_y = stats.gaussian_kde(historical_series)(kde_x)
        
        # Scale KDE to match histogram frequencies
        kde_y_scaled = kde_y * len(historical_series) * ((max(historical_series) - min(historical_series)) / bins)

        fig.add_trace(go.Scatter(
            x=kde_x,
            y=kde_y_scaled,  # Match KDE with histogram scale
            mode="lines",
            line=dict(color="black", width=2),
            name=f"KDE - {title}"
        ), row=row, col=col)

        # Latest Range Vertical Line (Extends Full Height)
        fig.add_trace(go.Scatter(
            x=[latest_data, latest_data],
            y=[0, max(kde_y_scaled) * 1.1],  # Scale the height slightly above KDE max
            mode="lines",
            line=dict(color="red", width=2, dash="dash"),
            name=f"Latest Range: {latest_data:.2f}"
        ), row=row, col=col)

    def plot_daily_range_distributions(self):
        """
        Generates and displays interactive histograms for daily range distributions over
        different timeframes (1 month, 3 months, 6 months, 12 months).
        """
        # Create a 2x2 subplot layout
        fig = make_subplots(
            rows=2, cols=2, 
            subplot_titles=[
                "Daily Range Distribution - 1 Month",
                "Daily Range Distribution - 3 Months",
                "Daily Range Distribution - 6 Months",
                "Daily Range Distribution - 1 Year"
            ]
        )

        # Data for each histogram with different bin sizes
        data_list = [
            (self.df_last_20_days, self.latest_range, 5, "1 Month"),
            (self.df_last_60_days, self.latest_range, 7, "3 Months"),
            (self.df_last_120_days, self.latest_range, 10, "6 Months"),
            (self.df_last_240_days, self.latest_range, 15, "1 Year")
        ]

        # Loop through each dataset and call the function
        for i, (historical_series, latest_data, bins, title) in enumerate(data_list):
            row = (i // 2) + 1  # Row index (1-based)
            col = (i % 2) + 1    # Column index (1-based)
            self.interactive_histogram(historical_series, latest_data, bins, title, row, col, fig)

        # Add x-axis and y-axis labels to each subplot
        for i in range(1, 3):  # Rows 1 and 2
            for j in range(1, 3):  # Columns 1 and 2
                fig.update_xaxes(title_text="Daily Range Bins", row=i, col=j)
                fig.update_yaxes(title_text="Frequency", row=i, col=j)

        # Update layout
        fig.update_layout(
            title="Daily Range Distributions with KDE",
            height=900, width=1100,
            showlegend=False,
            paper_bgcolor="white",  # White background
            plot_bgcolor="white",
        )

        # Show the interactive plot
        fig.show()

