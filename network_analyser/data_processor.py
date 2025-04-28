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
    SELECTED_FEATURES = ["Bwd Packet Length Mean","Avg Bwd Segment Size","Packet Length Variance",
         "Packet Length Mean","Average Packet Size","Packet Length Std","Bwd Packet Length Std",
         "Max Packet Length","Subflow Bwd Bytes","Total Length of Bwd Packets","Fwd IAT Max",
         "Bwd Packet Length Max","Flow IAT Std","Idle Max","Destination Port","Fwd IAT Total",
         "Fwd IAT Std","Bwd Packets/s",
    ]
    
    SELECTED_FEATURES2 = ['Total Backward Packets', 'Packet Length Variance', 'Flow IAT Std',
       'Fwd IAT Mean', 'Total Length of Bwd Packets', 'Max Packet Length',
       'Bwd IAT Max', 'Flow IAT Max', 'Avg Bwd Segment Size', 'Idle Mean',
       'Idle Max', 'Bwd Packet Length Mean', 'Average Packet Size',
       'Subflow Bwd Bytes', 'Fwd Header Length', 'Packet Length Mean',
       'Init_Win_bytes_forward', 'Fwd IAT Max', 'Fwd IAT Std',
       'Bwd Packet Length Std', 'Subflow Fwd Packets', 'Total Fwd Packets',
       'Bwd Packet Length Max', 'Bwd Packets/s', 'Packet Length Std',
       'Init_Win_bytes_backward', 'Flow Packets/s', 'Fwd IAT Total',
       'Destination Port', 'Subflow Bwd Packets'
    ]


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
        if input_df is not None:
            df = input_df
        else:
            df = self.df.copy()

        if df is None:
            raise ValueError("[ERROR] DataFrame is None. Please check the input file.")
        return df[
            [col for col in selected_features if col in df.columns]
        ]

    def normalise_data(self, features): 
        scaler = MinMaxScaler() 
        return scaler.fit_transform(features) # normalise data between 0 and 1


# for train purpose
    def get_benign(self, input_df=None):
        if input_df is not None:
            df = input_df
        else:
            df = self.df.copy()

        return df[df["Label"] == 0].drop(columns=["Label"])

    def split_data(self, input_df=None, test_size=0.3):
        if input_df is not None:
            df = input_df
        else:
            df = self.df

        x = df
        y = self.df["Label"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=42, shuffle=True,
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

