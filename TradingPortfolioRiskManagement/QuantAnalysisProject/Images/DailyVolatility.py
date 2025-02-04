import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DailyVolatilityVisualiser:
    """
    A class for visualizing daily volatility profiles using Seaborn histograms and KDE.
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
        self.latest_index = df.index[0]  # Latest range index

    def plot_daily_range_distributions(self):
        """
        Generates and displays Seaborn histograms with KDE for daily range distributions 
        over different timeframes (1 month, 3 months, 6 months, 12 months).
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Daily Range Distributions with KDE", fontsize=16, fontweight="bold")

        # Data for each histogram
        data_list = [
            (self.df_last_20_days, "1 Month", axes[0, 0]),
            (self.df_last_60_days, "3 Months", axes[0, 1]),
            (self.df_last_120_days, "6 Months", axes[1, 0]),
            (self.df_last_240_days, "1 Year", axes[1, 1])
        ]

        for historical_series, title, ax in data_list:
            # Histogram without border boxes
            sns.histplot(
                historical_series, kde=True, bins=10, ax=ax,
                color="blue", alpha=0.6
            )
            
            # Add vertical red dashed line for the latest range
            ax.axvline(self.latest_range, color="red", linestyle="dashed", linewidth=2, label=f"Daily Range: {self.latest_index}")
            
            # Annotate latest range value rounded to 2 decimal places
            ax.text(self.latest_range, ax.get_ylim()[1] * 0.9, f"{self.latest_range:.2f}", 
                    color="red", fontsize=10, fontweight="bold", ha="right")

            ax.set_title(f"Daily Range Distribution - {title}", fontsize=12, fontweight="bold")
            ax.set_xlabel("Daily Range Bins")
            ax.set_ylabel("Frequency")

            # Remove top and right box lines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        # Create a single legend for all subplots
        handles, labels = axes[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper right", fontsize=12, title="Legend", frameon=False)

        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit suptitle
        plt.show()
