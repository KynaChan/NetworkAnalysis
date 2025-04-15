import os
import subprocess

import cicflowmeter
import joblib


import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split


class NetworkAnomalyDetector:
    
    
    # Capture network traffic using tcpdump.
    def capture_traffic(self, interface="eth0", count=200, output_file="capture.pcap"):
        command = f"sudo tcpdump -i {interface} -w {output_file} -c {count}"
        subprocess.run(command, shell=True)
        print(f"[SUCCESS] Traffic captured and saved to {output_file}\n")


    # Transform the captured data with CICFlowMeter.
    def transform_data(
        self, input_file="captured_data.pcap", output_file="transformed_data.csv"
    ):
        print(f"[SUCCESS] Data transformed and saved to {output_file}\n")


    def preprocess_data(self, file_path):
        print("Data preprocessed")
        return df
