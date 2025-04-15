import pandas as pd
import numpy as np


class NetworkDataProcessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
        self.features: pd.DataFrame | None = None
        self.labels: pd.DataFrame | None = None
        

    def process(self):
        return self.data

    def clean_data(self):
        # Drop duplicates
        self.data.drop_duplicates(inplace = True)
        

        self.features = self.data.drop(columns=['label'])
        self.labels = self.data['label']
        
        
        # Check for missing values
        missing_values = self.features.isna().sum()
        if missing_values.any():
            print(f"[WARNING] Missing values found in the dataset:\n{missing_values}")

        # Replace infinite values with NaN
        self.features.replace([np.inf, -np.inf], np.nan, inplace=True)

        
        print(f"[SUCCESS] Data cleaned. Missing values handled.\n")



    def transform_data(self):
        # Placeholder for transformation logic
        return self.data
    
    
    
    