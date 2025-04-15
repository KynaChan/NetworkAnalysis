
import os
import subprocess

import numpy as np
import pandas as pd
import joblib
import cicflowmeter

from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split


class AnomalyDetector:
    # Capture network traffic using tcpdump.
    def capture_traffic(self, interface='eth0', count=100, output='capture.pcap'):
        command = f"sudo tcpdump -i {interface} -w {output} -c {count}"
        subprocess.run(command, shell=True)
        print(f"[SUCCESS] Traffic captured and saved to {output}\n")

    # Transform the captured data with CICFlowMeter.
    def extract_features(self, input_file='capture.pcap', output_file='transformed_data.csv'):


        print(f"[SUCCESS] Data transformed and saved to {output_file}\n")


    def preprocess_data(self, file_path):
        print("Data preprocessed")
        return df
    


