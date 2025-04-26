

import pandas as pd

from sklearn.ensemble import RandomForestClassifier


class AnomalyClassifier: 

    def __init__(self, model: RandomForestClassifier, identified_anomalies_df: pd.DataFrame):
        self.rf_model = model
        self.prep_data = identified_anomalies_df

    def run(self) -> pd.DataFrame:
        try:
            self.classify_anomalies()
            return self.get_anomaly_port_df()

        except Exception as e:
            raise Exception(f"\n  [ERROR] An error occurred: {e}\n")


    def classify_anomalies(self):
        if self.rf_model is None:
            raise ValueError("[ERROR] Model not provided.")
        self.prep_data['prediction'] = self.rf_model.predict(self.prep_data)


    def get_anomaly_port_df(self):
        if self.rf_predictions is None:
            raise ValueError("[ERROR] No predictions available. Run classify_anomalies() first.")
        
        # Create a DataFrame with the predictions and ports
        port_columns = [col for col in self.prep_data.columns if 'port' in col]
        anomaly_df = pd.DataFrame({
            "predictions": self.prep_data['prediction']==1,
            "ports": self.prep_data[port_columns]
        })
        anomaly_ports = anomaly_df[anomaly_df['predictions'] == 1]['anomaly_ports'].unique()
        return anomaly_ports