
from .model_trainer import IfModelTrainer, KMeansModelTrainer, RfModelTrainer

from .network_sniffer import NetworkSniffer
from .data_processor import DataProcessor
from .model_io import ModelIO
from .anomaly_classifier import AnomalyClassifier
from .anomaly_detector import AnomalyDetector
from .port_mapper import PortMapper

import os.path
import pandas as pd

class App:

    # MODEL_PATH= "trained_models/"
    IF_MODEL_NAME = "default_if_model.joblib"
    KMEANS_MODEL_NAME = "default_kmeans_model.joblib"
    RF_MODEL_NAME = "default_rf_model.joblib"

    # analyse network with pre-trained model
    # analyse network with loaded model
    # train model with offline data 
    # possible features: train model with live data (with labels?)

    def analyse_offline_traffic_with_specified_models_return_ports(self, offline_data_path, if_model_name, kmeans_model_name, rf_model_name):
        """
        Analyze offline data using specified models.

        Parameters:
            offline_data_path (str): Path to the offline data file. The data should be labeled and preprocessed with CICFlowMeter
            if_model_path (str): Path to the Isolation Forest model
            kmeans_model_path (str): Path to the KMeans model
            rf_model_path (str): Path to the Random Forest model
        """
        if_model, kmeans_model, rf_model = self._load_models(if_model_name, kmeans_model_name, rf_model_name)
        if_df, kmeans_df = self._process_test_data(offline_data_path)
        print("\n  [INFO] Start analysing traffic... \n")

        anomaly_ports_list = self._detect_anomaly_ports(if_model, if_df, kmeans_model, kmeans_df, rf_model)
        print(f"\n  [INFO] Anomaly ports detected: {anomaly_ports_list}")
        self._save_anomaly_ports_to_csv(anomaly_ports_list)
        return anomaly_ports_list


    def analyse_live_traffic_with_default_models_return_processes(self, interface, packet_count):
        """
        Capture network traffic and analyze it using default models.

        Parameters:
            interface (str): Network interface to capture traffic from
            packet_count (int): Number of packets to capture
        """
        return self.analyse_network_with_specified_models_return_processes(
            interface, packet_count, self.IF_MODEL_NAME, self.KMEANS_MODEL_NAME, self.RF_MODEL_NAME
        )
        
    def analyse_network_with_specified_models_return_processes(self, interface, packet_count, if_model_path, kmeans_model_path,rf_model_path):
        """
        Capture network traffic and analyze it using specified models.

        Parameters:
            interface (str): Network interface to capture traffic from
            packet_count (int): Number of packets to capture
            if_model_path (str): Path to the Isolation Forest model
            rf_model_path (str): Path to the Random Forest model
        """
        if_model, kmeans_model, rf_model = self._load_models(if_model_path, kmeans_model_path, rf_model_path)

        df = NetworkSniffer().run(interface, packet_count)

        if_df, kmeans_df = self._process_test_data(df)
        anomaly_ports_list = self._detect_anomaly_ports(if_model, if_df, kmeans_model, kmeans_df, rf_model)
        
        mapper = PortMapper()
        return mapper.get_port_info(anomaly_ports_list)


    def train_models_with_offline_data_default_setting(self, offline_data_path: str):
        """
        Preprocess offline data and train new models.

        Parameters:
            offline_data_path (str): Path to the offline data file. The data should be labeled and preprocessed with CICFlowMeter
        """
        dp = DataProcessor(offline_data_path)
        dp.clean_data()
        selected_features = dp.get_features() 
        benign_df = dp.get_benign()
        benign_selected_features = dp.get_features(benign_df)

        kmeans_prep_data = dp.normalise_data(selected_features)
        kmeans_prep_bengin_data = dp.normalise_data(benign_selected_features)

        print("\n  [INFO] Start training Isolation Forest... \n")
        # Train the model using the processed features
        if_trainer = IfModelTrainer(benign_selected_features)
        if_model = if_trainer.train_if_model(n_estimators=300, contamination=0.3)
        if_model.predict(selected_features)

        print("\n  [INFO] Start training K-Means... \n")
        kmeans_trainer = KMeansModelTrainer(kmeans_prep_bengin_data)
        kmeans_model = kmeans_trainer.train_kmeans_model(n_clusters=10)
        kmneas_distances = kmeans_model.transform(kmeans_prep_data)

        rf_df = selected_features.copy()
        rf_df["anomaly_scores"] = -if_model.decision_function(selected_features)
        rf_df["kmeans_distances"] = kmneas_distances.min(axis=1)

        print("\n  [INFO] Start training Random Forest... \n")
        x_train, x_test, y_train, y_test = dp.split_data(rf_df)
        rf_trainer = RfModelTrainer(x_train, x_test, y_train, y_test)
        rf_model = rf_trainer.train_model(n_estimators=300)
        rf_trainer.test_model()

        m_io = ModelIO()
        model_path = "trained_models/"
        models = [
            (if_model, "if_model"),
            (kmeans_model, "kmeans_model"),
            (rf_model, "rf_model"),
        ]
        for model, model_name in models:
            model_path_name = f"{model_path}{model_name}.joblib"
            checked_file_name = self._check_file_exists(model_path_name)
            m_io.save_model(model, checked_file_name)

        print("\n  [SUCCESS] Models trained and saved successfully.\n")
    
    def train_models_with_live_data(self, interface, packet_count):
        pass


# private functions
    def _load_models(self, if_model_path, kmeans_model_path, rf_model_path):
        m_io = ModelIO()
        if_model = m_io.load_model(if_model_path)
        kmeans_model = m_io.load_model(kmeans_model_path)
        rf_model = m_io.load_model(rf_model_path)
        return if_model,  kmeans_model,rf_model

    def _process_test_data(self, df):
        # k_drop_cols = ['Destination Port',  ]
        dp = DataProcessor(df)
        dp.clean_data()
        if_df = dp.get_features()
        # kmeans_prep_df = if_df.drop(columns=k_drop_cols)
        kmeans_df = dp.normalise_data(if_df)
        return if_df, kmeans_df

    def _detect_anomaly_ports(self, if_model,if_df, kmeans_model, kmeans_df, rf_model):
        rf_df= AnomalyDetector(if_model, if_df, kmeans_model, kmeans_df).run()
        rf_classifier = AnomalyClassifier(rf_model, rf_df)
        return rf_classifier.run()
    
    def _check_file_exists(self, file_name):
        base, ext = os.path.splitext(file_name)
        counter = 1
        new_file_name = file_name
        while os.path.exists(new_file_name):
            new_file_name = f"{base}_{counter}{ext}"
            counter += 1
        return new_file_name
    

    def _save_anomaly_ports_to_csv(self, anomaly_ports_list, process_name=None, anomaly_score=None):
        anomaly_ports_df = pd.DataFrame(anomaly_ports_list, columns=["Port"]) # can None be added to the columns?
        file_path = "outputs/"
        file_name = "anomaly_ports_list.csv"
        checked_name = self._check_file_exists(file_path+file_name)
        anomaly_ports_df.to_csv(checked_name, index=False)
        print(f"\n  [INFO] Anomaly ports saved to {checked_name}. \n")