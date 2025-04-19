
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

class RfDataParams:
    XTrain = None
    XTest = None
    YTrain = None
    YTest = None


class DataProcessor:

    SELECTED_FEATURES = ["ip","yum","pudding","bubble tea"]

    def __init__(self, csv):
        self.df = pd.read_csv(csv) 
        if self.df.empty:
            raise ValueError("\n  [ERROR] DataFrame is empty. Please check the input file.\n")

        # Strip whitespace from column names
        self.df = self.df.columns.str.strip()


        # self.features: pd.DataFrame | None = None
        self.labels: pd.DataFrame | None = None



# Main function to process data
    def process_rf_data(self) -> RfDataParams:

        self.process_data()
        x_train, x_test, y_train, y_test = self.split_data()
        
        
        rf_data = RfDataParams()
        rf_data.XTrain = x_train
        rf_data.XTest = x_test
        rf_data.YTrain = y_train
        rf_data.YTest = y_test
        
        return rf_data

    def process_data(self):
        self.select_features()
        self.remove_duplicates()
        self.convert_invalid()
        self.handle_missing()
        self.drop_label()




# Additional layer of feature selection
    def select_features(self, selected_features = SELECTED_FEATURES):

        # EDIT: select features by keywords
        self.features = self.df[[col for col in selected_features if col in self.df.columns]] 
        
        print(f"\n  [SUCCESS] Features selected: {self.features.columns}\n")




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




# Model specific steps

    # Drop 'Label' column
    def drop_label(self):

        # save labels
        self.labels = self.features['Label']

        if 'Label' in self.features.columns:
            self.features.drop(columns=['Label'], inplace=True)
            print(f"\n  [SUCCESS] 'Label' column dropped.\n")
        else:
            print(f"\n  [INFO] No 'Label' column found to drop.\n")

    # Split data into training and testing sets
    def split_data(self, test_size=0.3):
        if self.features is None or self.labels is None:
            raise ValueError("\n  [ERROR] Features or labels not found.\n")
        
        x = self.features
        y = self.labels
        
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)
        
        return x_train, x_test, y_train, y_test


