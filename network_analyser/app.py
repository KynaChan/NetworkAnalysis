
import model_trainer

import network_sniffer
import data_processor
import model_io
import feature_selector
import anomaly_classifier
import anomaly_detector
import port_mapper

import pandas as pd


class NetworkAnalyser:
  
    # analyse network with pre-trained model
    # analyse network with loaded model

    # train model with offline data 

    # possible features: train model with live data (with labels?)


    def analyse_network_with_default_models(self, interface, packet_count):
        """
        Capture network traffic and analyze it using default models.

        Parameters:
            interface (str): Network interface to capture traffic from
            packet_count (int): Number of packets to capture
        """
        return self.analyse_network_with_specified_models(interface, packet_count, "model/def_if_model", "model/def_rf_model")


    def analyse_network_with_specified_models(self, interface, packet_count, if_model_path,rf_model_path):
        """
        Capture network traffic and analyze it using specified models.

        Parameters:
            interface (str): Network interface to capture traffic from
            packet_count (int): Number of packets to capture
            if_model_path (str): Path to the Isolation Forest model
            rf_model_path (str): Path to the Random Forest model
        """
        if_model = model_io.load_model(if_model_path)
        rf_model = model_io.load_model(rf_model_path)

        df = network_sniffer.run(interface, packet_count)

        dp = data_processor.DataProcessor(df)
        dp.clean_data()
        prep_data = dp.get_features()
        
        new_df= anomaly_detector.run(if_model, prep_data)

        rf_classifier = anomaly_classifier.AnomalyClassifier(rf_model, new_df)
        anomaly_ports_list = rf_classifier.run()
        
        mapper = port_mapper.PortMapper()
        return mapper.get_port_info(anomaly_ports_list)



    def train_models_with_offline_data_default_setting(self, offline_data_path: str):
        """
        Preprocess offline data and train new models.

        Parameters:
            offline_data_path (str): Path to the offline data file. The data should be labeled and preprocessed with CICFlowMeter
        """

        dp = data_processor.DataProcessor(offline_data_path)
        dp.clean_data()
        benign_df = dp.get_benign() # benign df with label

        if_prep_bengin_data = dp.get_features(benign_df)
        kmeans_prep_bengin_data = dp.standardise_data(benign_df)

        x_train, x_test, y_train, y_test = dp.split_data()
        
        # Train the model using the processed features
        if_trainer = model_trainer.IfModelTrainer(if_prep_bengin_data)
        if_model = if_trainer.train_if_model(n_estimators=300, contamination=0.3)

        kmeans_trainer = model_trainer.KMeansModelTrainer(kmeans_prep_bengin_data)
        kmeans_model = kmeans_trainer.train_kmeans_model(n_clusters=2)

        rf_trainer = model_trainer.RfModelTrainer(x_train, x_test, y_train, y_test)
        rf_model = rf_trainer.train_model(n_estimators=300)

        model_io.save_model(if_model, "model/def_if_model")
        model_io.save_model(rf_model, "model/def_rf_model")
        model_io.save_model(kmeans_model, "model/def_kmeans_model")

        print("\n  [SUCCESS] Models trained and saved successfully.\n")
        return if_model, rf_model, kmeans_model