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
eval $(poetry env activate)

python3 main.py
```
## CLI
```shell
Network Sniffer and Analyser

options:
  -h, --help            show this help message and exit
  -m {train,detect}, --mode {train,detect}
                        Mode of operation: 'train' to train models, 'detect' to detect anomalies.
  -n {offline,live}, --network_type {offline,live}
                        Network type: 'offline' to use offline data, 'live' to capture live network traffic. (default: offline)
  -i INTERFACE, --interface INTERFACE
                        Network interface to capture traffic from (default: eth0)
  -c COUNT, --count COUNT
                        Number of packets to capture (default: 100)
  -t TRAIN_FILE, --train_file TRAIN_FILE
                        Path to the training data file (you can add your file to path: traffic_data/training_data/)
  -f FLOW_FILE, --flow_file FLOW_FILE
                        Path to the offline data file (you can add your file to path: traffic_data/)
  -if IF_MODEL_NAME, --if_model_name IF_MODEL_NAME
                        Path to the Isolation Forest model file (default: if_model.joblib)
  -kmeans KMEANS_MODEL_NAME, --kmeans_model_name KMEANS_MODEL_NAME
                        Path to the KMeans model file (default: kmeans_model.joblib)
  -rf RF_MODEL_NAME, --rf_model_name RF_MODEL_NAME
                        Path to the Random Forest model file (default: rf_model.joblib)
```

## Links & References

Dataset used: [Network Intrusion dataset(CIC-IDS- 2017)](https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset)


