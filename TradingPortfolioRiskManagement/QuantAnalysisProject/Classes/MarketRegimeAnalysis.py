import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class MarketRegimeAnalysis:
    """
    A class for analyzing market regimes using the Hurst exponent and visualizing trends.
    """

    def __init__(self, df):
        """
        Initializes the MarketRegimeAnalysis class.

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
        Computes the Hurst exponent for each trading day and classifies the market regime.

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

                    # Classify market behavior
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
        Generates static Seaborn plots for:
        - Market regime classification counts.
        - Hurst exponent over time with a shaded Random Walk zone.
        """
        # Ensure trends are analyzed before plotting
        if not self.hurst_values_by_date:
            self.analyze_trends()

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle("Market Regime Analysis", fontsize=16, fontweight="bold")

        ### 🔹 Bar Chart: Market Regime Counts ###
        sns.barplot(
            x=list(self.market_regime_counts.keys()),
            y=list(self.market_regime_counts.values()),
            ax=axes[0],
            palette=["#1f77b4", "#4c72b0", "#6baed6"]  # Different shades of blue
        )

        # Label the bars with counts
        for container in axes[0].containers:
            axes[0].bar_label(container, fmt='%d', fontsize=12, padding=3)

        axes[0].set_title("Market Regime Counts", fontsize=14, fontweight="bold")
        axes[0].set_xlabel("Market Type")
        axes[0].set_ylabel("Count")

        # Remove top and right spines
        axes[0].spines['top'].set_visible(False)
        axes[0].spines['right'].set_visible(False)

        ### 🔹 Scatter Plot: Hurst Exponent Over Time ###
        sns.scatterplot(
            x=self.hurst_df["date"],
            y=self.hurst_df["hurst"],
            hue=self.hurst_df["market_type"],
            palette={"Mean-Reverting": "#1f77b4", "Random Walk": "#4c72b0", "Trending": "#6baed6"},
            ax=axes[1],
            s=50  # Adjust marker size
        )

        # Fill area for Random Walk Zone (0.49 - 0.51)
        axes[1].fill_between(
            self.hurst_df["date"], 0.49, 0.51, color="gray", alpha=0.2, label="Random Walk Zone"
        )

        # Add a horizontal dashed line at 0.5 for reference
        axes[1].axhline(y=0.5, color="gray", linestyle="dashed", linewidth=1)

        axes[1].set_title("Hurst Exponent Over Time", fontsize=14, fontweight="bold")
        axes[1].set_xlabel("Date")
        axes[1].set_ylabel("Hurst Exponent")

        # Rotate x-axis labels for readability
        axes[1].tick_params(axis='x', rotation=45)

        # Remove top and right spines
        axes[1].spines['top'].set_visible(False)
        axes[1].spines['right'].set_visible(False)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
