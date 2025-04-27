# Network Anomaly Detector

## Overview
todo: add project desc here



## Setup

This project uses [Poetry](https://python-poetry.org/) to manage virtual environments and dependencies.

To setup and run the tool, run the following commands in order (WSL 2.0, Ubuntu):


Install poetry as a system-wide command tool.
```shell
sudo apt update && apt install python3-poetry
```

Make sure you are in the project's root location and run the following command to install the dependecies and initial venv setup.
```shell
poetry install
```

Run with poetry:
```shell
poetry run python main.py
```

Or run within venv:
```shell
poetry shell

python3 main.py
```
## CLI
```shell
Network Sniffer and Analyser

options:
  -h, --help            show this help message and exit
  -m {train,detect,detect_live}, --mode {train,detect,detect_live}
                        Mode of operation: 'train' to train models, 'detect' to detect anomalies, 'detect_live' to capture live
                        traffic to detect anomalies.
  -i INTERFACE, --interface INTERFACE
                        Network interface to capture traffic from (default: eth0)
  -c COUNT, --count COUNT
                        Number of packets to capture (default: 100)
  -t TRAIN_FILE, --train_file TRAIN_FILE
                        Path to the training data file (default path: traffic_data/training_data/)
  -f FLOW_FILE, --flow_file FLOW_FILE
                        Path to the offline data file (default path: traffic_data/)
  -if IF_MODEL_PATH, --if_model_path IF_MODEL_PATH
                        Path to the Isolation Forest model file (default: trained_models/default_if_model.joblib)
  -kmeans KMEANS_MODEL_PATH, --kmeans_model_path KMEANS_MODEL_PATH
                        Path to the KMeans model file (default: trained_models/default_kmeans_model.joblib)
  -rf RF_MODEL_PATH, --rf_model_path RF_MODEL_PATH
                        Path to the Random Forest model file (default: trained_models/default_rf_model.joblib)
```

## Links & References

Dataset used: [Network Intrusion dataset(CIC-IDS- 2017)](https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset)


