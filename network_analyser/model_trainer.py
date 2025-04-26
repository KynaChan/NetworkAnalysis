
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest, RandomForestClassifier


class IfModelTrainer:
    """
    Train Isolation Forest model for anomaly detection.

    Parameters:
        if_prep_data (pd.DataFrame): Preprocessed data for training the Isolation Forest model.
    """
    def __init__(self, if_prep_data):
        self.if_prep_data = if_prep_data # begnin with the preprocessed data

    def train_if_model(self, n_estimators=None, contamination=None):
        return IsolationForest(
            n_estimators=n_estimators, contamination=contamination
        ).fit(self.if_prep_data)


class KMeansModelTrainer:
    """
    Train KMeans model for anomaly detection.

    Parameters:
        kmeans_prep_data (pd.DataFrame): Preprocessed (and normalised) data for training the KMeans model.
    """
    def __init__(self, kmeans_prep_data):
        self.kmeans_prep_data = kmeans_prep_data

    def train_kmeans_model(self, n_clusters=None):
        return KMeans(n_clusters=n_clusters).fit(self.kmeans_prep_data)




class RfModelTrainer:
    """
    Train Random Forest model for anomaly classification.

    Parameters:
        x_train (pd.DataFrame): Training features.
        x_test (pd.DataFrame): Testing features.
        y_train (pd.Series): Training labels.
        y_test (pd.Series): Testing labels.
    """

    def __init__(self, x_train,x_test, y_train, y_test):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

        self.rf_model = None

    def train_model(self, n_estimators=None):
        # Train Random Forest model

        self.rf_model = RandomForestClassifier(n_estimators=n_estimators)
        self.rf_model.fit(self.x_train, self.y_train, shuffle=True)

        return self.rf_model

    def test_model(self):
        # Predict on the test set
        y_pred = self.rf_model.predict(self.x_test)

        # Calculate accuracy
        accuracy = self.rf_model.accuracy_score(self.y_test, y_pred)
        print(f"\n  [SUCCESS] Random Forest model trained with accuracy: {accuracy:.2f}\n")
        print(self.rf_model.classification_report(self.y_test, y_pred))
        return y_pred
    
    def get_feature_imp_score(self):
        # Get feature importances
        return self.rf_model.feature_importances_

