

from sklearn.ensemble import RandomForestClassifier


class AnomalyClassifier: 

    def __init__(self, model = None, identified_anomalies=None):
        self.rf_model = model | None
        self.identified_anomalies = identified_anomalies | None

        self.rf_predictions = None


    def classify_anomalies(self):
        if self.rf_model is None:
            raise ValueError("\n  [ERROR] Model not provided.\n")
        
        # Predict anomalies using the Isolation Forest model
        self.rf_predictions = self.rf_model.predict(self.identified_anomalies)
        
        return self.rf_predictions
    
    # where to extract anomaly ports?