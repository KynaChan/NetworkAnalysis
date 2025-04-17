import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import IsolationForest, RandomForestClassifier

class ModelTrainer:
    def __init__(self, preprocessed_data: pd.DataFrame, labels):
        self.if_model = None
        self.rf_model = None
        self.sur_model = None
        self.if_prediction = None
        self.rf_prediction = None

        self.df = preprocessed_data | None
        self.labels = labels | None


    
    def train_if_model(self, n_estimators=None, contamination=None):

        # Train Isolation Forest model
        if_model = IsolationForest(n_estimators=n_estimators, contamination=contamination)
        if_model.fit(self.df)

        # # Predict anomalies      
        # if self.labels is not None:
        #     y_pred = if_model.predict(self.df)
        #     accuracy = accuracy_score(y, y_pred)
        #     print(f"\n  [SUCCESS] Isolation Forest model trained with accuracy: {accuracy:.2f}\n")
        #     print(classification_report(y, y_pred))

        self.if_prediction = if_model.predict(self.df)
        self.if_model = if_model
        return self.if_model # should i return

    def train_rf_model(self, n_estimators=None):

        # Train Random Forest model
        rf_model = RandomForestClassifier(n_estimators=n_estimators)
        rf_model.fit(self.df, self.labels)
        
        # # Predict on the test set        ? do i export x_train y_train etc from DataProcessor ?
        # y_pred = rf_model.predict(x_test)
        
        # # Calculate accuracy             ? do i do this here or evaluator ? 
        # accuracy = accuracy_score(y_test, y_pred)
        # print(f"\n  [SUCCESS] Random Forest model trained with accuracy: {accuracy:.2f}\n")
        # print(classification_report(y_test, y_pred))

        # self.rf_prediction = rf_model.predict(self.df)    # split? 
        self.rf_model = rf_model
        return self.rf_model # should i return



    # should this be in this class or evaluator?
    # model to get importance scores (for feature selection)
    # might need one for rf_model too
    def train_surrogate_model(self):         
        self.if_prediction = pd.Series(self.if_prediction).map({-1: 1,1: 0})
    
        sur_model = RandomForestClassifier()
        sur_model.fit(self.df, self.if_prediction)
        self.sur_model = sur_model

    def derive_importances(self, model):
        return


 

