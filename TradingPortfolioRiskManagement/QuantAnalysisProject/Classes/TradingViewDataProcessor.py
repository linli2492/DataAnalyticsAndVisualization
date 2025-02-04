#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd

class TradingViewDataProcessor:
    def __init__(self, file_path, export_name):
        """
        Initializes the class with the CSV file path.

        Parameters:
        file_path (str): Path to the CSV file.
        """
        self.file_path = file_path
        self.export_name = export_name
        self.df = None  # Placeholder for DataFrame

    def process_data(self, extract_time = False):
        """
        Reads the CSV file, processes the data, and returns a cleaned DataFrame.

        Steps:
        1. Load the CSV into a Pandas DataFrame.
        2. Convert UNIX timestamp to a human-readable datetime.
        3. Extract date-related columns (day, month, year, etc.).
        4. Sort the DataFrame in descending order by datetime.
        5. Drop unnecessary columns (`datetime`, `time`).
        6. Set `date` as the index.
        """
        # Load CSV file
        self.df = pd.read_csv(self.file_path)

        # Convert UNIX timestamp to datetime (assuming 'time' column contains the timestamp)
        self.df['datetime'] = pd.to_datetime(self.df['time'], unit="s")
        
        if extract_time:
            self.df['timestamp'] = self.df['datetime'].dt.time

        # Extract date components
        self.df['date'] = self.df['datetime'].dt.date                      # Extract Date (YYYY-MM-DD)
        self.df['day_of_week'] = self.df['datetime'].dt.day_name()         # Extract Day of the Week (e.g., Monday)
        self.df['month_num'] = self.df['datetime'].dt.month                # Extract Month as a Number (1-12)
        self.df['month_name'] = self.df['datetime'].dt.month_name()        # Extract Month as a String (e.g., December)
        self.df['year'] = self.df['datetime'].dt.year                      # Extract Year (YYYY)
        
        # Calculate the range (High - Low)
        self.df['range'] = self.df['high'] - self.df['low']

        # Sort DataFrame by datetime in descending order
        self.df = self.df.sort_values(by='datetime', ascending=False)

        # Drop unnecessary columns
        self.df = self.df.drop(columns=['datetime', 'time'], errors='ignore')  

        # Set 'date' as the index
        self.df = self.df.set_index('date')
        
        self.df.columns = self.df.columns.str.title()
        
        self.df.to_csv(self.export_name, index = False, sep = ";", encoding = "utf-8")

        return self.df

