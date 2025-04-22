import psutil


class PortMapper:
    """A class that maps network ports to their corresponding processes."""
    # pass a df with prediction & ports
    # then use the port column to get process
    # process info will be add to the df as a new column
    # return df 
    def __init__(self, ports: list[int]):
        """
        Initialize PortMapper with a list of ports to analyze.

        Args:
            ports (List[int]): List of port numbers to analyze
        """
        self.ports = ports
        self.port_info: list[dict] = []

# rename
    def get_port_info(self) -> list[dict]:
        """
        Get information about processes running on the specified ports.

        Returns:
            List[Dict]: List of dictionaries containing process information
                       Each dict has 'port', 'pid', 'name', and 'cmdline' keys
        """
        self.port_info.clear()

        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port in self.ports:
                try:
                    process = psutil.Process(conn.pid)
                    self.port_info.append(
                        {
                            "port": conn.laddr.port,
                            "pid": conn.pid,
                            "name": process.name(),
                            "cmdline": process.cmdline(),
                            "create_time": process.create_time(),
                            "status": process.status(),
                            "username": process.username()
                        }
                    )
                    
                except psutil.AccessDenied:
                    # Handle the case where access to process information is denied
                    self.port_info.append(
                        {
                            "port": conn.laddr.port,
                            "pid": conn.pid,
                            "name": None,
                            "cmdline": None,
                            "create_time": None,
                            "status": None,
                            "username": None
                        }
                    )
                except psutil.NoSuchProcess:
                    continue

        return self.port_info
