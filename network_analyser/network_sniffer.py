
import os
import subprocess

import pandas as pd

class NetworkSniffer: 
    """A class to capture and transform network traffic data.
    This class provides methods to capture network traffic using tcpdump
    and transform the captured data using CICFlowMeter.
    """
    
    
    def __init__(self, interface='eth0', count=100):
        self.interface = interface
        self.count = count

        self.pcap_file_path = "traffic_data/captured_traffic.pcap"

        self.output_df: pd.DataFrame | None = None

    def run(self) -> pd.DataFrame:
        try:
            self.capture_traffic()
            self.rewrite_pcap()
            self.transform_traffic_data()

            return self.output_df

        except Exception as e:
            raise Exception(f"\n  [ERROR] An error occurred: {e}\n")

    # Capture network traffic using tcpdump.
    def capture_traffic(self):
        print("Capturing network traffic...")
        
        
        cmd = ["tcpdump", "-i", self.interface, "-c", str(self.count), "-w", self.pcap_file_path]
        subprocess.run(cmd)

        # Check if the output file was created successfully
        if not os.path.exists(self.pcap_file_path):
            raise FileNotFoundError(f"\n  [ERROR] Output file {self.pcap_file_path} was not created.\n")
        
        print(f"\n  [SUCCESS] Traffic captured and saved to {self.pcap_file_path}. (Packet count: {self.count})\n")
        
    # rewrite pcap file to add ethernet layer
    def rewrite_pcap(self):
        # tcprewrite --dlt=enet --infile="training_data/pcap/file_name.pcap" --outfile="training_data/pcap/file_name_eth.pcap"
        # subprocess.run(["tcprewrite", "--dlt=enet", "--infile=" + self.pcap_file_path, "--outfile=" + self.pcap_file_path])
        pass


    # Transform raw pcap to csv using CICFlowMeter
    def transform_traffic_data(self, output_file="transformed_data.csv"): 
        cmd = ["cicflowmeter", "-f", self.pcap_file_path, "-c", output_file] 
        subprocess.run(cmd) 
        # Check if the output file was created successfully
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"[ERROR] Output file {output_file} was not created.")
        
        # Read the transformed data into a DataFrame
        self.df = pd.read_csv(output_file)
        print(f"\n  [SUCCESS] Data transformed and saved to {output_file}.\n")

        # Check if the DataFrame is empty
        if self.df.empty:
            raise ValueError("[ERROR] The DataFrame is empty after transformation.")

