import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans


class AnomalyDetector: # need one more prep data for kmeans
    """
    Initialize the AnomalyDetector with the Isolation Forest model and preprocessed data.
    
    Parameters:
        if_model (IsolationForest): Pre-trained Isolation Forest model.
        if_prep_data (pd.DataFrame): Preprocessed data for anomaly detection.
        kmeans_model (KMeans): Pre-trained KMeans model.
        kmeans_prep_data (pd.DataFrame): Preprocessed data for KMeans clustering.
    """
    def __init__(self, if_model: IsolationForest, if_prep_data: pd.DataFrame,kmeans_model: KMeans,kmeans_prep_data):

        self.if_model = if_model
        self.kmeans_model = kmeans_model
        self.if_prep_data = if_prep_data
        self.kmeans_prep_data = kmeans_prep_data

        self.if_preds = pd.DataFrame(columns=["raw_prediction", "prediction"])
        self.anomalies = None
        self.benign = None



    def run(self) -> pd.DataFrame:
        try:
            if_scores = self.if_identify_anomalies()
            kmeans_distances = self.kmeans_identify_anomalies()
            return self.if_prep_data.assign(
                anomaly_scores=if_scores, kmeans_distances=kmeans_distances
            )

        except Exception as e:
            raise Exception(f"\n  [ERROR] An error occurred: {e}\n")


# check unit test for this class
    def if_identify_anomalies(self):
        if self.if_model is None or self.if_prep_data is None:
            raise ValueError("[ERROR] Model or processed data not provided.\n")

        # .predict() returns 1 for normal and -1 for anomalies
        self.if_preds['raw_prediction'] = self.if_model.predict(self.if_prep_data)
        self.if_preds['prediction'] = self.if_preds['raw_prediction'].map({1: 0, -1: 1})

        return -self.if_model.decision_function(self.if_prep_data)

    # def get_anomaly_score_df(self):
        
    def kmeans_identify_anomalies(self):
        if self.kmeans_model is None or self.kmeans_prep_data is None:
            raise ValueError("[ERROR] Model or processed data not provided.\n")

        # .predict() returns the cluster label for each sample
        distances = self.kmeans_model.transform(self.kmeans_prep_data)
        return distances.min(axis=1)

    # def get_kmeans_distances(self):


    # # extract anomalies and clean up df
    # def extract_anomalies_df(self):
    #     if self.prep_data is None:
    #         raise ValueError("[ERROR] No processed data available. Run identify_anomalies() first.")

    #     self.anomalies = self.prep_data[self.prep_data['prediction'] == 1]
    #     self.anomalies = self.anomalies.drop(columns=['raw_prediction', 'prediction'])

    #     print(f"[SUCCESS] Anomalies identified: {len(self.anomalies)}\n")
    #     return self.anomalies

    # def extract_benign_df(self):
    #     if self.prep_data is None:
    #         raise ValueError("[ERROR] No processed data available. Run identify_anomalies() first.")

    #     self.benign = self.prep_data[self.prep_data['prediction'] == 0]
    #     self.benign = self.benign.drop(columns=['raw_prediction', 'prediction'])

    #     print(f"[SUCCESS] Benign instances identified: {len(self.benign)}\n")
    #     return self.benign


