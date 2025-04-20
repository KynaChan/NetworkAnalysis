import pandas as pd
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self, model: IsolationForest, prep_data: pd.DataFrame):
        self.if_model = model
        self.prep_data = prep_data

        self.if_predictions = None
        self.anomalies = None
        self.benign = None


    def identify_anomalies(self):
        if self.if_model is None or self.prep_data is None:
            raise ValueError("[ERROR] Model or processed data not provided.\n")

        # Predict anomalies using the Isolation Forest model
        self.if_predictions = self.if_model.predict(self.prep_data)

        self.anomalies = self.prep_data[self.if_predictions == -1]  # do i need this?
        self.benign = self.prep_data[self.if_predictions == 1]

        print(f"[SUCCESS] Anomalies identified: {len(self.anomalies)}\n")
        print(f"[SUCCESS] Benign instances identified: {len(self.benign)}\n")


    def transform_predictions(self):
        if self.if_predictions is None:
            raise ValueError("\n  [ERROR] No predictions to transform.\n")

        if_predictions = pd.Series(self.if_predictions).map({1: 0, -1: 1})
        return if_predictions
