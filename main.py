


from network_analyzer.network_sniffer import NetworkSniffer
from network_analyzer.port_mapper import PortMapper

def main():
    print("Starting Network Sniffer...")
    
    port_mapper = PortMapper([80, 443, 22, 8080, 8000, 3306])
    print(port_mapper.get_port_info())
    
    network_sniffer = NetworkSniffer(interface="wlo1")
    df = network_sniffer.run()
    


if __name__ == "__main__":
    main()
