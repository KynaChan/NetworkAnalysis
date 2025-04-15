
import os
import subprocess

import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split


class AnomalyDetector:

    def capture_traffic(self, interface='eth0', duration=10, output_file='traffic.pcap'):
        """
        Capture network traffic using tcpdump.
        """
        command = f"sudo tcpdump -i {interface} -w {output_file} -G {duration} -W 1"
        subprocess.run(command, shell=True)
        print(f"Traffic captured and saved to {output_file}")
        return output_file

    def preprocess_data(self, file_path):
        """
        Preprocess the captured data.
        """
        # This is a placeholder for actual preprocessing logic.
        # In a real scenario, you would parse the pcap file and extract features.
        # For demonstration, we will create a dummy dataset.
        data = {
            'src_ip': np.random.randint(1, 255, size=100),
            'dst_ip': np.random.randint(1, 255, size=100),
            'src_port': np.random.randint(1, 65535, size=100),
            'dst_port': np.random.randint(1, 65535, size=100),
            'protocol': np.random.choice(['TCP', 'UDP'], size=100),
            'length': np.random.randint(40, 1500, size=100)
        }
        df = pd.DataFrame(data)
        print("Data preprocessed")
        return df
    


