
import os
import subprocess

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split


class PcapProcessor:

    SELECTED_FEATURES = ["ip","yum","pudding","bubble tea"]

    def __init__(self, pcap_file_path: str):
        self.pcap_file_path = pcap_file_path

        self.df: pd.DataFrame | None = None
        self.features: pd.DataFrame | None = None
        self.labels: pd.DataFrame | None = None

    # Return the processed DataFrame.
    def preprocess(self, type: str = "train") -> pd.DataFrame:
        
        # transform the data
        # select features
        # remove duplicates
        # convert invalid values to NaN
        # handle missing values

        # do i drop and split here??
        
        
        return # wht to return??

# Coversion and feature selection steps

    # Transform raw pcap to csv using CICFlowMeter
    def transform_data(self, output_file="transformed_data.csv"): 
        cmd = ["cicflowmeter", "-f", self.pcap_file_path, "-c", output_file] 
        subprocess.run(cmd) 
        # Check if the output file was created successfully
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"\n  [ERROR] Output file {output_file} was not created.\n")
        
        # Read the transformed data into a DataFrame
        self.df = pd.read_csv(output_file)
        print(f"\n  [SUCCESS] Data transformed and saved to {output_file}.\n")

        # Check if the DataFrame is empty
        if self.df.empty:
            raise ValueError(f"\n  [ERROR] The DataFrame is empty after transformation.\n")
        
        
        
    # Additional feature selection
    def select_features(self, selected_features = SELECTED_FEATURES):

        # EDIT: select features by keywords
        self.features = self.df[[col for col in selected_features if col in self.df.columns]] 
        
        print(f"\n  [SUCCESS] Features selected: {self.features.columns}\n")


    def process_training_data(self, pcap_file_path: str) -> pd.DataFrame:
        output_df = N
        
        return None
    
    def process_testing_data(self, pcap_file_path: str) -> pd.DataFrame:
        return None


# Data cleaning steps
    # Remove duplicates
    def remove_duplicates(self):
        self.features.drop_duplicates(inplace=True)
        print(f"\n  [SUCCESS] Duplicates removed. {self.df.shape[0]} rows remaining.\n")
    
    # Convert invalid values to NaN
    def convert_invalid(self):
        self.features.replace([np.inf, -np.inf], np.nan, inplace=True)
        print(f"\n  [SUCCESS] Invalid values converted to NaN.\n")

    # Handle missing values 
    def handle_missing(self):
        # Fill missing values with the mean of each column
        self.features.interpolate(inplace=True)
        print(f"\n  [SUCCESS] Missing values filled with column means.\n")

    # Drop 'Label' column
    def drop_label(self):
        # save labels
        self.labels = self.features[' Label']

        if 'label' in self.features.columns:
            self.features.drop(columns=['label'], inplace=True)
            print(f"\n  [SUCCESS] 'Label' column dropped.\n")
        else:
            print(f"\n  [INFO] No 'Label' column found to drop.\n")

    # Split data into training and testing sets
    def split_data(self, test_size=0.3):
        # Split the data into features and labels
        x = self.features
        y = self.labels
        
        # Split the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)
        
        # Return the split data
        return x_train, x_test, y_train, y_test




    


    

    
    
    
    