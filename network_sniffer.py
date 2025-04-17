
import os
import subprocess


class NetworkSniffer: 

    # Capture network traffic using tcpdump.
    def capture_traffic(self, interface='eth0', count=100, output_file='captured_data.pcap'):
        cmd = ["tcpdump", "-i", interface, "-c",count, "-w", output_file]
        subprocess.run(cmd)

        # Check if the output file was created successfully
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"\n  [ERROR] Output file {output_file} was not created.\n")
        
        print(f"\n  [SUCCESS] Traffic captured and saved to {output_file}. (Packet count: {count})\n")