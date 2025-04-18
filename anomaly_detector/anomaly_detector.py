
import subprocess

import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest


class AnomalyDetector:

    def __init__(self, model, processed_data):
        self.if_model = model
        self.processed_data = processed_data

        self.if_predictions = None
        self.anomalies = None
        self.benign = None


    def identify_anomalies(self):
        if self.if_model is None or self.processed_data is None:
            raise ValueError("\n  [ERROR] Model or processed data not provided.\n")

        # Predict anomalies using the Isolation Forest model
        self.if_predictions = self.if_model.predict(self.processed_data)

        # Separate anomalies and benign instances
        self.anomalies = self.processed_data[self.if_predictions == -1]
        self.benign = self.processed_data[self.if_predictions == 1]

        print(f"\n  [SUCCESS] Anomalies identified: {len(self.anomalies)}\n")
        print(f"\n  [SUCCESS] Benign instances identified: {len(self.benign)}\n")
        return self.anomalies # do i return the benign instances too?

    def save_anomalies(self, output_file="anomalies.csv"):
        if self.anomalies is None:
            raise ValueError("\n  [ERROR] No anomalies to save.\n")

        # Save anomalies to a CSV file
        self.anomalies.to_csv(output_file, index=False)
        print(f"\n  [SUCCESS] Anomalies saved to {output_file}\n")
