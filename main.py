
from anomaly_detector.network_sniffer import NetworkSniffer

def main():
    print("Starting Network Sniffer...")
    
    network_sniffer = NetworkSniffer()
    df = network_sniffer.run()
    


if __name__ == "__main__":
    main()
