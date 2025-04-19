
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


class FeatureSelector:
    TOP_N = 20 

    def __init__(
            self, detected_anomalies="" | pd.Series, 
            rf_imp_scores=""| np.ndarray, 
            prep_data=""| pd.DataFrame
        ):

        self.detected_anomalies = detected_anomalies
        self.rf_imp_scores = rf_imp_scores

        self.feature_names = prep_data.columns
# need for both model, but prep_data for rf_model is split randomly, do i take another arg for rf_prep_data?
        
        self.selected_features = None

    

    def compute_if_model_imp_scores(self):
        """
        A surrogate model, using Random Forest, to select features based on their importance.
        """
        if self.detected_anomalies is None or self.detected_anomalies.empty:
            raise ValueError("\n  [ERROR] No detected anomalies to compute importance scores.\n")
        
        rf_model = RandomForestClassifier()
        rf_model.fit(self.feature_names, self.detected_anomalies)

        return rf_model.feature_importances_

        
    def rank_features(self, feature_importances):

        # Sort features by importance
        sorted_indices = feature_importances.argsort()[::-1]
        
        # Select top N features (e.g., top 10)
        self.selected_features = sorted_indices[:10]


        # # Sort features by importance scores
        # sorted_features = sorted(self.importance_scores.items(), key=lambda x: x[1], reverse=True)
        # self.selected_features = [feature for feature, score in sorted_features[:top_n]]
