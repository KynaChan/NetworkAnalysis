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
        choices=["train", "detect"],
        help="Mode of operation: 'train' to train models, 'detect' to detect anomalies.",
    )
    parser.add_argument(
        "-n",
        "--network_type",
        type=str,
        default="offline",
        choices=["offline", "live"],
        help="Network type: 'offline' to use offline data, 'live' to capture live network traffic. (default: offline)",
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
        default="concat_train.csv",
        help="Path to the training data file (you can add your file to path: traffic_data/training_data/)",
    )
    parser.add_argument(
        "-f",
        "--flow_file",
        type=str,
        default="concat_test.csv",
        help="Path to the offline data file (you can add your file to path: traffic_data/)",
    )
    parser.add_argument(
        "-if",
        "--if_model_name",
        type=str,
        default="if_model.joblib",
        help="Path to the Isolation Forest model file (default: if_model.joblib)",
    )
    parser.add_argument(
        "-kmeans",
        "--kmeans_model_name",
        type=str,
        default="kmeans_model.joblib",
        help="Path to the KMeans model file (default: kmeans_model.joblib)",
    )
    parser.add_argument(
        "-rf",
        "--rf_model_name",
        type=str,
        default="rf_model.joblib",
        help="Path to the Random Forest model file (default: rf_model.joblib)",
    )

    args = parser.parse_args()

    interface = args.interface
    packet_count = args.count
    mode = args.mode
    network_type = args.network_type
    train_file = TRAINING_FILE_PATH+args.train_file
    flow_file = TRAFFIC_FILE_PATH+args.flow_file
    if_model_path = MODEL_FILE_PATH+args.if_model_name
    kmeans_model_path = MODEL_FILE_PATH+args.kmeans_model_name
    rf_model_path = MODEL_FILE_PATH+args.rf_model_name


    app = App()

    if mode == "train":
        if network_type == "offline":
            app.train_models_with_offline_data_default_setting(train_file)
        elif network_type == "live":
            pass
            # app.train_models_with_live_data(interface, packet_count)

    elif mode == "detect":
        if network_type == "offline":
            app.analyse_offline_traffic_with_specified_models_return_ports(flow_file, if_model_path, kmeans_model_path, rf_model_path)
        elif network_type == "live":
            app.analyse_network_with_specified_models_return_processes(interface, packet_count, if_model_path, kmeans_model_path, rf_model_path)

    else:
        print("Invalid mode. Try to use 'train' or 'detect'.")


if __name__ == "__main__":
    main()
