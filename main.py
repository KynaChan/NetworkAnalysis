import argparse

from network_analyser.app import App

TRAFFIC_FILE_PATH = "traffic_data/"
TRAINING_FILE_PATH = "traffic_data/training_data/"
MODEL_FILE_PATH = "trained_models/"


def main():
    """
    Main function to run the network sniffer and analyser application.
    It uses argparse to parse command line arguments for different modes of operation.
    The available modes are:
    - train: Train models with offline data
    - detect: Detect anomalies in offline data using pre-trained
      models
    - detect_live: Capture live network traffic and detect anomalies using pre-trained models
    """

    parser = argparse.ArgumentParser(description="Network Sniffer and Analyser")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["train", "detect", "detect_live"],
        help="Mode of operation: 'train' to train models, 'detect' to detect anomalies, 'detect_live' to capture live traffic to detect anomalies.",
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        default="eth0",
        help="Network interface to capture traffic from (default: eth0)",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=100,
        help="Number of packets to capture (default: 100)",
    )
    parser.add_argument(
        "-t",
        "--train_file",
        type=str,
        # default=TRAINING_FILE_PATH + "concat_train.csv",
        help="Path to the training data file (default path: traffic_data/training_data/)",
    )
    parser.add_argument(
        "-f",
        "--flow_file",
        type=str,
        # default=TRAFFIC_FILE_PATH + "concat_test.csv",
        help="Path to the offline data file (default path: traffic_data/)",
    )
    parser.add_argument(
        "-if",
        "--if_model_path",
        type=str,
        default=MODEL_FILE_PATH + "default_if_model.joblib",
        help="Path to the Isolation Forest model file (default: trained_models/default_if_model.joblib)",
    )
    parser.add_argument(
        "-kmeans",
        "--kmeans_model_path",
        type=str,
        default=MODEL_FILE_PATH + "default_kmeans_model.joblib",
        help="Path to the KMeans model file (default: trained_models/default_kmeans_model.joblib)",
    )
    parser.add_argument(
        "-rf",
        "--rf_model_path",
        type=str,
        default=MODEL_FILE_PATH + "default_rf_model.joblib",
        help="Path to the Random Forest model file (default: trained_models/default_rf_model.joblib)",
    )

    args = parser.parse_args()

    interface = args.interface
    packet_count = args.count
    mode = args.mode
    train_file = args.train_file
    flow_file = args.flow_file
    if_model_path = MODEL_FILE_PATH + "default_if_model.joblib"
    kmeans_model_path = MODEL_FILE_PATH + "default_kmeans_model.joblib"
    rf_model_path = MODEL_FILE_PATH + "default_rf_model.joblib"


    app = App()
    if mode == "train":
        app.train_models_with_offline_data_default_setting(train_file, model_tag="default")
    elif mode == "detect":
        app.analyse_offline_traffic_with_default_models_return_ports(flow_file)
    elif mode == "detect_live":
        app.analyse_live_traffic_with_default_models_return_processes(interface, packet_count)
    elif mode == "detect_live":
        app.analyse_network_with_specified_models(interface, packet_count, if_model_path, kmeans_model_path, rf_model_path)
        

    else:
        print("Invalid mode. Try to use 'train' or 'detect'.")


if __name__ == "__main__":
    main()
