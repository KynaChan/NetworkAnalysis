from unittest.mock import Mock, patch

import psutil

from network_analyser.port_mapper import PortMapper
import socket, os


def test_port_mapper_initialization():
    ports = [80, 443]
    mapper = PortMapper(ports)
    assert mapper.ports == ports
    assert mapper.port_info == []


def test_get_port_info_empty_when_no_connections():
    with patch("psutil.net_connections", return_value=[]):
        mapper = PortMapper([80])
        result = mapper.get_port_info()
        assert result == []


def test_get_port_info_filters_unmatched_ports():
    mock_conn = Mock(laddr=Mock(port=8080), pid=123)
    with patch("psutil.net_connections", return_value=[mock_conn]):
        mapper = PortMapper([80])
        result = mapper.get_port_info()
        assert result == []


def test_get_port_info_handles_process_exceptions():
    mock_conn = Mock(laddr=Mock(port=80), pid=123)
    with patch("psutil.net_connections", return_value=[mock_conn]):
        with patch("psutil.Process", side_effect=psutil.NoSuchProcess(123)):
            mapper = PortMapper([80])
            result = mapper.get_port_info()
            assert result == []

def test_get_port_info_returns_correct_data():
    # Start a simple HTTP server in a separate process
    
    # Create a socket that will listen on port 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    
    try:
        # Create PortMapper instance
        mapper = PortMapper([8080])
        result = mapper.get_port_info()
        
        # Verify that we found our socket
        assert len(result) == 1
        assert result[0]['port'] == 8080
        assert result[0]['pid'] == os.getpid()
        assert result[0]['name'] == psutil.Process().name()
    
    finally:
        # Clean up
        server_socket.close()
