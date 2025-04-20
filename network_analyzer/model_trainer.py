
import pandas as pd
import RfDataParams


from sklearn.ensemble import IsolationForest, RandomForestClassifier


class IfModelTrainer:

    def __init__(self, if_prep_data):
        self.df = preprocessed_data
        self.labels = labels


    def train_if_model(self, n_estimators=None, contamination=None):
        return IsolationForest(
            n_estimators=n_estimators, contamination=contamination
        ).fit(self.df)



class RfModelTrainer:

    def __init__(self, rf_prep_data: RfDataParams):
        self.rf_prep_data = rf_prep_data

    def train_model(self, n_estimators=None):
        # Train Random Forest model

        rf_model = RandomForestClassifier(n_estimators=n_estimators)
        rf_model.fit(self.df, self.labels)

        return rf_model


    def test_model(self, rf_model, x_test, y_test):
        # Predict on the test set
        y_pred = rf_model.predict(x_test)

        # Calculate accuracy
        accuracy = rf_model.accuracy_score(y_test, y_pred)
        print(f"\n  [SUCCESS] Random Forest model trained with accuracy: {accuracy:.2f}\n")
        print(rf_model.classification_report(y_test, y_pred))
        return y_pred

