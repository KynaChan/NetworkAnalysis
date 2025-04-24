
import pandas as pd


from sklearn.ensemble import IsolationForest, RandomForestClassifier


class IfModelTrainer:

    def __init__(self, if_prep_data):
        self.if_prep_data = if_prep_data
        # self.labels = labels

    def train_if_model(self, n_estimators=None, contamination=None):
        return IsolationForest(
            n_estimators=n_estimators, contamination=contamination
        ).fit(self.if_prep_data)



class RfModelTrainer:

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

