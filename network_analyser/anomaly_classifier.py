

from sklearn.ensemble import RandomForestClassifier


class AnomalyClassifier: 

    def __init__(self, model: RandomForestClassifier, identified_anomalies):
        self.rf_model = model
        self.identified_anomalies = identified_anomalies

        self.rf_predictions = None


    def classify_anomalies(self):
        if self.rf_model is None:
            raise ValueError("[ERROR] Model not provided.")
        
        # Predict anomalies using the Isolation Forest model
        self.rf_predictions = self.rf_model.predict(self.identified_anomalies)
        
        return self.rf_predictions
    
    def get_anomaly_ports(self):
        if self.rf_predictions is None:
            raise ValueError("[ERROR] No predictions made yet.")
        
        # Get the indices of the anomalies
        anomaly_indices = [i for i, x in enumerate(self.rf_predictions) if x == -1]
        
        # Get the corresponding ports
        anomaly_ports = [self.identified_anomalies[i] for i in anomaly_indices]
        
        return anomaly_ports