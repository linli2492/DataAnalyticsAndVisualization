import pandas as pd
import numpy as np
from datetime import datetime
import os
import psycopg2

class FuturesDataProcessor:
    """
    Processes raw futures data from a CSV file, formats it for database storage,
    and provides methods to handle data by date.

    Attributes
    ----------
    file : str
        Path to the raw data file.
    futures_name : str
        Name of the futures contract.
    df : pd.DataFrame
        DataFrame containing processed data.

    Methods
    -------
    data_processor()
        Reads, cleans, and processes the CSV file, then saves the data to a new CSV.
    split_by_date()
        Splits the data into individual DataFrames by unique date and returns them in a dictionary.
    """

    def __init__(self, file):
        """
        Initializes the FuturesDataProcessor class with the provided file path.

        Parameters
        ----------
        file : str
            Path to the raw futures data CSV file.
        """
        self.futures_name = None
        self.file = file
        self.df = pd.DataFrame()
    
    def data_processor(self):
        """
        Reads the raw data file, processes date and time columns, filters rows based on date count,
        and saves the processed data as a new CSV.

        Returns
        -------
        None
        """
        # Read the file with semicolon separators for the rest of the columns
        df = pd.read_csv(self.file, sep=';', header=None,
                         names=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])

        # Split 'DateTime' into 'Date' and 'Time' based on space delimiter
        df[['Date', 'Time']] = df['DateTime'].str.split(' ', expand=True)

        # Convert 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

        # Format 'Time' to include leading zeros and convert to datetime time format
        df['Time'] = df['Time'].apply(lambda x: f"{int(x):06d}")
        df['Time'] = pd.to_datetime(df['Time'], format='%H%M%S').dt.time

        # Combine 'Date' and 'Time' into a single 'DateTime' column
        df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

        # Set 'DateTime' as the index and drop the original 'Date', 'Time', and 'DateTime' columns
        df.set_index('DateTime', inplace=True)
        df.drop(columns=['Date', 'Time'], inplace=True)
        
        # Filter to include only dates with more than 1000 rows to ensure we have a complete day's worth of price data
        df['date_only'] = df.index.date 
        date_counts = df['date_only'].value_counts()
        valid_dates = date_counts[date_counts > 1000].index  
        df = df[df['date_only'].isin(valid_dates)]  
        df.drop(columns=['date_only'], inplace=True)  
        
        # Save the processed DataFrame as a CSV file ready to upload to SQL 
        base_name = os.path.basename(self.file).split('.')[0]
        output_file = f"{base_name}.csv"
        self.df = df
        self.df.to_csv(output_file, index = True)
        print(f"{base_name} successfully processed into a CSV")
        self.futures_name= base_name
        
        return output_file, self.df
  
    def split_by_date(self):
        """
        Splits the DataFrame into individual DataFrames by date and stores them in a dictionary.

        Returns
        -------
        tuple
            A dictionary of DataFrames by date and a list of unique dates.
        """
        dfs_by_date = {}
        date_list = []

        # Get unique dates from the DateTime index
        dates = pd.unique(self.df.index.date)

        # Split the DataFrame by each unique date
        for date in dates:
            date_str = date.strftime('%Y-%m-%d')
            df_by_date = self.df[self.df.index.date == date]
            dfs_by_date[date_str] = df_by_date
            date_list.append(date_str)
        
        print(f"{self.futures_name} put into a dictionary of dataframes split by dates")

        return dfs_by_date, date_list
    
class FuturesPostgreSQLUploader:
    """
    Connects to a PostgreSQL database, loads futures data from CSV, and inserts it into the database.

    Attributes
    ----------
    db_config : dict
        Database configuration dictionary with keys for host, database, user, and password.
    csv_file : str
        Path to the CSV file with processed futures data.
    df : pd.DataFrame
        DataFrame to hold CSV data for processing.
    conn : psycopg2.connection
        Database connection object.
    cursor : psycopg2.cursor
        Database cursor for executing SQL commands.

    Methods
    -------
    connect_to_db()
        Establishes a connection to the PostgreSQL database.
    load_csv()
        Loads data from the CSV file into a DataFrame.
    insert_futures()
        Inserts futures name into the futures_table, returning the futures_id.
    insert_datetime(datetime_value)
        Inserts a datetime into datetime_table if it doesn't exist, returning the datetime_id.
    insert_all_datetimes()
        Inserts all unique datetimes from the DataFrame into datetime_table.
    insert_price_data(futures_id)
        Inserts OHLCV price data into price_table using the futures_id.
    close_connection()
        Closes the database connection and cursor.
    """
    
    def __init__(self, db_config, csv_file):
        """
        Initializes the FuturesPostgreSQLUploader class with database configuration and CSV file path.

        Parameters
        ----------
        db_config : dict
            Database configuration with keys 'host', 'database', 'user', and 'password'.
        csv_file : str
            Path to the CSV file containing futures data.
        """
        self.host = db_config["host"]
        self.database = db_config["database"]
        self.user = db_config["user"]
        self.password = db_config["password"]
        self.csv_file = csv_file
        self.df = pd.DataFrame()
        self.conn = None
        self.cursor = None
        self.futures_name = None
        
    def connect_to_db(self):
        """
        Establishes a connection to the PostgreSQL database and creates a cursor.

        Returns
        -------
        None
        """
        try:
            self.conn = psycopg2.connect(host = self.host, 
                                        database = self.database,
                                        user = self.user, 
                                        password = self.password)
            self.cursor = self.conn.cursor()
            print("Connection to database successful.")
        except Exception as e: 
            print(f"Failed to connect to database: {e}")
        
    def load_csv(self):
        """
        Loads the data from the specified CSV file into a DataFrame.

        Returns
        -------
        None
        """
        self.df = pd.read_csv(self.csv_file)
        self.df['DateTime'] = pd.to_datetime(self.df['DateTime'], format='%Y/%m/%d %H:%M:%S')
        self.futures_name = os.path.basename(self.csv_file).split('.')[0]
        print(f"{self.futures_name} data loaded from CSV.")
        
    def insert_futures(self):
        """
        Inserts the futures name into the futures_table, or retrieves the futures_id if it already exists.

        Returns
        -------
        int or None
            The futures_id if successful, or None on failure.
        """
        try:
            # Check if futures already exists in the table
            self.cursor.execute(
            """
            SELECT futures_id 
            FROM futures_table 
            WHERE futures = %s
            """,
            (self.futures_name,))
            result = self.cursor.fetchone()

            if result:
                futures_id = result[0]
            else:
                # Insert new futures name of retrieve its ID
                self.cursor.execute(
                """
                INSERT INTO futures_table (futures)
                VALUES (%s)
                RETURNING futures_id
                """, 
                (self.futures_name,))
                futures_id = self.cursor.fetchone()[0]
                if futures_id:
                    self.conn.commit()
                print(f"Inserted futures name '{self.futures_name}' with ID {futures_id}")
            
            return futures_id
        
        except Exception as e:
            self.conn.rollback()  # Rollback transaction on error
            print(f"Failed to insert futures: '{self.futures_name}': {e}")
            return None
        
    def insert_datetime(self, datetime_value):
        """
        Inserts a datetime into datetime_table if it doesn't already exist.

        Parameters
        ----------
        datetime_value : datetime
            The datetime value to insert.

        Returns
        -------
        int or None
            The datetime_id if successful, or None on failure.
        """
        # Convert numpy.datetime64 to Python datetime if necessary
        if isinstance(datetime_value, np.datetime64):
            datetime_value = datetime.utcfromtimestamp((datetime_value - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's'))
        
        # Check if datetime already exists in the table
        self.cursor.execute(
        """
        SELECT datetime_id
        FROM datetime_table
        WHERE datetime = %s
        """,
        (datetime_value,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            # Insert new datetime if it doesn't exist and retrieve it's ID
            self.cursor.execute(
            """
            INSERT INTO datetime_table(datetime)
            VALUES (%s)
            RETURNING datetime_id
            """,
            (datetime_value,))
            return self.cursor.fetchone()[0]
        
    def insert_all_datetimes(self):
        """
        Inserts all unique datetimes from the DataFrame into datetime_table.

        Returns
        -------
        None
        """
        if 'DateTime' not in self.df.columns:
            print("No 'DateTime' column found in the DataFrame.")
            return
        
        unique_datetimes = self.df['DateTime'].unique()
        for datetime_value in unique_datetimes:
            self.insert_datetime(datetime_value)
            
        self.conn.commit()
        print("All unique datetimes inserted.")
        
    def insert_price_data(self, futures_id):
        if futures_id is None:
            print("Invalid futures_id (None), cannot insert price data.")
            return
        
        if self.df.empty:
            print("DataFrame is empty, nothing to insert.")
            return
        
        for _, row in self.df.iterrows():
            #get or insert datetime_id
            datetime_id = self.insert_datetime(row['DateTime'])
            if datetime_id is None:
                print(f"Failed to get datetime_id for DateTime {row['DateTime']}. Skipping this row.")
                continue
                
            try:
                self.cursor.execute(
                """
                INSERT INTO price_table (futures_id, datetime_id, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (futures_id, datetime_id, row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))
            
            except Exception as e:
                print(f"Failed to insert price data for datetime '{row['DateTime']}': {e}")
        
        self.conn.commit()
        print("All OHLCV price data inserted.")   
        
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")


