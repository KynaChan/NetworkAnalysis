import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler



class DataProcessor:
    """
        Initialize the DataProcessor with a file path or a DataFrame.
        If a DataFrame is provided, it will be used directly. Otherwise, the file path will be used to load the data.
        
        Parameters:
            data_file_path (str): Path to the CSV file containing the data.
            dataframe (pd.DataFrame): DataFrame containing the data. If provided, this will be used instead of loading from a file.
        
        Functions:
            - load_data_path: Load data from a CSV file.
            - clean_data: Clean the data by formatting columns, removing duplicates, converting invalid values, and handling missing values.
            - get_benign: Get benign data from the DataFrame.
            - get_features: Get selected features from the DataFrame.
            - normalise_data: Normalize the data using MinMaxScaler.
            - split_data: Split the data into training and testing sets.
    """
    SELECTED_FEATURES = ["ip", "yum", "pudding", "bubble tea"]

    def __init__(self, data_file_path:str=None, dataframe: pd.DataFrame = None):

        self.df = dataframe or self.load_data_path(data_file_path)
        assert self.df is not None, "[ERROR] DataFrame is None. Please check the input file."


    def load_data_path(self, data_file_path: str) -> pd.DataFrame:
        """Load data from a CSV file."""
        df = pd.read_csv(data_file_path)

        if df.empty:
            raise ValueError("[ERROR] DataFrame is empty. Please check the input file.")
        return df


# for train and detection purpose
    def get_features(self, input_df=None, selected_features=SELECTED_FEATURES):
        df = input_df or self.df
        if df is None:
            raise ValueError("[ERROR] DataFrame is None. Please check the input file.")
        return df[
            [col for col in selected_features if col in df.columns]
        ]

    def normalise_data(features): 
        scaler = MinMaxScaler() 
        return scaler.fit_transform(features) # normalise data between 0 and 1


# for train purpose
    def get_benign(self):
        return self.df[self.df["Label"] == 0]

    def split_data(self, test_size=0.3):
        x = self.get_features()
        y = self.df["Label"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=42
        )

        return x_train, x_test, y_train, y_test



# Main function to process data
    def clean_data(self):
        print("Cleaning data...")

        self._format_columns()
        self._convert_labels()
        self._remove_duplicates()
        self._convert_invalid()
        self._handle_missing()
        
        return self.df




# Data cleaning steps

    def _format_columns(self):
        self.df.columns = self.df.columns.str.strip()
        # self.df.columns.str.replace(" ", "_")

    # if lables are not binary, convert them to 0 and 1
    def _convert_labels(self):
        # Convert labels to binary values (0 and 1)
        if type(self.df["Label"].iloc[0]) == str:
            self.df["Label"] = self.df["Label"].apply(lambda x: 0 if x == 'BENIGN' else 1).astype(int)
            print("\n  [SUCCESS] Labels converted to binary values.\n")
        else:
            print("\n  [INFO] Labels are already in binary format.\n")

    # Remove duplicates
    def _remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)
        print(f"\n  [SUCCESS] Duplicates removed. {self.df.shape[0]} rows remaining.\n")

    # Convert invalid values to NaN
    def _convert_invalid(self):
        self.df.replace([np.inf, -np.inf], np.nan, inplace=True)
        print("\n  [SUCCESS] Invalid values converted to NaN.\n")

    # Handle missing values (drop labels avoid being affected
    def _handle_missing(self):
        labels = self.df["Label"]
        features = self.df.drop(columns=["Label"])

        features.interpolate(inplace=True)

        self.df = features.copy()
        self.df["Label"] = labels
        print("\n  [SUCCESS] Missing values filled with column means.\n")

