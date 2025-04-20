import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split



class DataProcessor:
    SELECTED_FEATURES = ["ip", "yum", "pudding", "bubble tea"]

    def __init__(self, data_file_path: str):
        self.df = self.load_data(data_file_path)


    def load_data(self, data_file_path: str) -> pd.DataFrame:
        """Load data from a CSV file."""
        df = pd.read_csv(data_file_path)

        if df.empty:
            raise ValueError("[ERROR] DataFrame is empty. Please check the input file.")

        return df


    def get_features(self, selected_features=SELECTED_FEATURES):
        return self.df[
            [col for col in selected_features if col in self.df.columns]
        ]


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
        self._remove_duplicates()
        self._convert_invalid()
        self._handle_missing()



# Data cleaning steps

    def _format_columns(self):
        self.df.columns.str.strip()
        # self.df.columns.str.replace(" ", "_")

    # Remove duplicates
    def _remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)
        print(f"\n  [SUCCESS] Duplicates removed. {self.df.shape[0]} rows remaining.\n")


    # Convert invalid values to NaN
    def _convert_invalid(self):
        self.df.replace([np.inf, -np.inf], np.nan, inplace=True)
        print("\n  [SUCCESS] Invalid values converted to NaN.\n")


    # Handle missing values
    def _handle_missing(self):
        # Fill missing values with the mean of each column
        self.df.interpolate(inplace=True)
        print("\n  [SUCCESS] Missing values filled with column means.\n")

