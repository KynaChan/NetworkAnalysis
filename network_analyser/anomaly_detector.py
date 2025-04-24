import pandas as pd
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self, model: IsolationForest, prep_data: pd.DataFrame):
        self.if_model = model
        self.prep_data = prep_data

        self.predictions = pd.DataFrame(columns=["raw_prediction", "prediction"])
        self.anomalies = None
        self.benign = None

    def run(self) -> pd.DataFrame:
        try:
            self.identify_anomalies()
            return self.get_anomaly_score_df()

        except Exception as e:
            raise Exception(f"\n  [ERROR] An error occurred: {e}\n")


# check unit test for this class
    def identify_anomalies(self):
        if self.if_model is None or self.prep_data is None:
            raise ValueError("[ERROR] Model or processed data not provided.\n")

        # .predict() returns 1 for normal and -1 for anomalies
        self.predictions['raw_prediction'] = self.if_model.predict(self.prep_data)
        self.predictions['prediction'] = self.predictions['raw_prediction'].map({1: 0, -1: 1})


    def get_anomaly_score_df(self):
        self.prep_data['anomaly_score'] = self.if_model.decision_function(self.prep_data)

        # Normalize the anomaly score to a range of 0 to 1
        # self.prep_data['anomaly_score'] = (self.prep_data['anomaly_score'] - self.prep_data['anomaly_score'].min()) / (
        #     self.prep_data['anomaly_score'].max() - self.prep_data['anomaly_score'].min()
        # )

        # Invert scores
        self.prep_data['anomaly_score'] = 1 - self.prep_data['anomaly_score']
        return self.prep_data
    


    # extract anomalies and clean up df
    def extract_anomalies_df(self):
        if self.prep_data is None:
            raise ValueError("[ERROR] No processed data available. Run identify_anomalies() first.")

        self.anomalies = self.prep_data[self.prep_data['prediction'] == 1]
        self.anomalies = self.anomalies.drop(columns=['raw_prediction', 'prediction'])

        print(f"[SUCCESS] Anomalies identified: {len(self.anomalies)}\n")
        return self.anomalies

    def extract_benign_df(self):
        if self.prep_data is None:
            raise ValueError("[ERROR] No processed data available. Run identify_anomalies() first.")

        self.benign = self.prep_data[self.prep_data['prediction'] == 0]
        self.benign = self.benign.drop(columns=['raw_prediction', 'prediction'])

        print(f"[SUCCESS] Benign instances identified: {len(self.benign)}\n")
        return self.benign


