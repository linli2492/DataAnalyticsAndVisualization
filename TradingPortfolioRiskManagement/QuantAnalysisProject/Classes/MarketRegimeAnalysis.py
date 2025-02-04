import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
import plotly.express as px
from statsmodels.tsa.stattools import adfuller

class MarketRegimeAnalysis:
    """
    A class for analyzing market regimes using the Hurst exponent and visualizing trends.
    """

    def __init__(self, df):
        """
        Initializes the TrendAnalysis class.

        Parameters:
        - df: Pandas DataFrame containing M5 OHLC data with 'Close' prices.
        """
        self.df = df
        self.df.index = pd.to_datetime(self.df.index)  # Ensure index is datetime
        self.unique_dates = list(self.df.index.floor('D').unique())[1:]  # Remove first date to avoid incomplete day
        
        # Storage for analysis results
        self.market_regime_counts = {"Mean-Reverting": 0, "Random Walk": 0, "Trending": 0}
        self.hurst_values_by_date = {}

    def hurst_exponent(self, series, max_lag=100):
        """
        Computes the Hurst exponent using the rescaled range method.

        Parameters:
        - series: Pandas Series of closing prices.
        - max_lag: Maximum lag for rescaled range calculation.

        Returns:
        - hurst: Hurst exponent value.
        """
        if len(series) < max_lag:
            return np.nan  # Avoid errors with small data

        lags = range(2, min(max_lag, len(series)))  # Adjust lags if data is short
        tau = [np.std(series[lag:] - series[:-lag]) for lag in lags]
        tau = np.array(tau)
        tau[tau == 0] = 1e-8  # Replace zero values to avoid log(0) issues

        hurst = np.polyfit(np.log(lags), np.log(tau), 1)[0]
        return hurst

    def analyze_trends(self):
        """
        Loops through each unique date in the dataset, computes the Hurst exponent,
        and classifies the market regime.

        Updates:
        - self.hurst_values_by_date
        - self.market_regime_counts
        """
        for date in self.unique_dates:
            daily_data = self.df[self.df.index.floor('D') == date]['Close']
            if not daily_data.empty:
                hurst_value = self.hurst_exponent(daily_data)

                if not np.isnan(hurst_value):
                    self.hurst_values_by_date[date] = hurst_value

                    # Classify market behavior based on updated thresholds
                    if hurst_value < 0.49:
                        self.market_regime_counts["Mean-Reverting"] += 1
                    elif 0.49 <= hurst_value <= 0.51:
                        self.market_regime_counts["Random Walk"] += 1
                    elif hurst_value > 0.51:
                        self.market_regime_counts["Trending"] += 1

        # Convert Dict to DataFrame for visualization
        self.hurst_df = pd.DataFrame(list(self.hurst_values_by_date.items()), columns=['date', 'hurst'])
        self.hurst_df['market_type'] = self.hurst_df['hurst'].apply(
            lambda x: "Mean-Reverting" if x < 0.49 else "Random Walk" if 0.49 <= x <= 0.51 else "Trending"
        )

    def plot_trend_analysis(self):
        """
        Generates interactive plots for market regime classification:
        - Bar chart showing the number of Mean-Reverting, Random Walk, and Trending Days.
        - Scatter plot visualizing the Hurst Exponent over time with a shaded Random Walk zone.
        """
        # Ensure trends are analyzed before plotting
        if not self.hurst_values_by_date:
            self.analyze_trends()

        # Interactive Bar Chart: Market Regime Counts
        fig_bar = px.bar(
            pd.DataFrame(self.market_regime_counts.items(), columns=['Market Type', 'Count']), 
            x='Market Type', y='Count', color='Market Type', text='Count',
            title="Number of Mean-Reverting, Random Walk, and Trending Days"
        )

        fig_bar.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=True
        )

        # Interactive Scatter Plot: Market Regime Over Time (With Line & Random Walk Zone)
        fig_time_series = go.Figure()

        # Add market regime time series as a line + scatter plot
        fig_time_series.add_trace(go.Scatter(
            x=self.hurst_df["date"],
            y=self.hurst_df["hurst"],
            mode="lines+markers",
            name="Hurst Exponent",
            marker=dict(color="black", size=5),
            line=dict(color="black", width=1.5)
        ))

        # Add Random Walk zone (0.49 - 0.51) as a filled area
        fig_time_series.add_trace(go.Scatter(
            x=self.hurst_df["date"].tolist() + self.hurst_df["date"].tolist()[::-1],
            y=[0.49] * len(self.hurst_df) + [0.51] * len(self.hurst_df),
            fill='toself',
            fillcolor="rgba(128, 128, 128, 0.3)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Random Walk Zone"
        ))

        # Add a horizontal dashed line at 0.5 for reference
        fig_time_series.add_trace(go.Scatter(
            x=self.hurst_df["date"],
            y=[0.5] * len(self.hurst_df),
            mode="lines",
            name="Threshold (0.5)",
            line=dict(color="gray", dash="dash")
        ))

        fig_time_series.update_layout(
            title="Market Regime Over Time (Hurst Exponent)",
            xaxis_title="Date",
            yaxis_title="Hurst Exponent",
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=True
        )

        # Show interactive plots
        fig_bar.show()
        fig_time_series.show()


# In[ ]:




