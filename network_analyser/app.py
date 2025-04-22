
import model_trainer

import network_sniffer
import data_processor
import model_io
import feature_selector
import anomaly_classifier
import anomaly_detector
import port_mapper

import pandas as pd
import numpy as np


class NetworkAnalyser:
  
  # analyse network with pre-trained model
  # analyse network with loaded model

  # train model with offline data
  # 

  # possible features: train model with live data (with labels?)
  
  

    def __init__(self):
        pass



    def analyse_network_with_default_models(self, interface, count):

        model = model_io.load_model(self.config['model_path'])
        
        # Start the network sniffer
        self.network = network_sniffer.start_sniffer(self.config['interface'])
        
        # Process the captured packets
        processed_data = data_processor.process_packets(self.network)
        
        # Extract features from the processed data
        features = feature_selector.extract_features(processed_data)
        
        # Classify anomalies using the pre-trained model
        anomalies = anomaly_classifier.classify_anomalies(model, features)
        
        return anomalies



    def analyse_network_with_specific_models(self, interface, packet_count, if_model_path,rf_model_path):

        if_model = model_io.load_model(if_model_path)
        rf_model = model_io.load_model(rf_model_path)

        df = network_sniffer.run(interface, packet_count)
        dp = data_processor.DataProcessor(df)
        dp.clean_data()
        
        # Extract features from the processed data
        prep_data = dp.get_features()
        
        if_detector = anomaly_detector.AnomalyDetector(if_model, prep_data)
        if_detector.identify_anomalies()
        detected_anomalies = if_detector.transform_predictions()

        rf_classifier = anomaly_classifier.AnomalyClassifier(rf_model, detected_anomalies)
        rf_predictions = rf_classifier.classify_anomalies()
        anomaly_ports = rf_classifier.get_anomaly_ports()
        
        mapper = port_mapper.PortMapper()
        anomaly_process = mapper.get_port_info(anomaly_ports)
        
        #create a dataframe with the results
        results_df = p
        return 



    def train_models_with_offline_data(self, offline_data_path: str):
        # Load the offline data
        offline_data = data_processor.load_offline_data(offline_data_path)
        
        # Process the offline data
        processed_data = data_processor.process_packets(offline_data)
        
        # Extract features from the processed data
        features = feature_selector.extract_features(processed_data)
        
        # Train the model using the processed features
        model = model_trainer.train_model(features, self.config['model_params'])
        
        # Save the trained model
        model_io.save_model(model, self.config['model_path'])
        
        return model