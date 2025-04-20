from unittest.mock import Mock, patch

import psutil

from network_analyzer.port_mapper import PortMapper


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
    mock_conn = Mock(laddr=Mock(port=80), pid=123)
    mock_process = Mock()
    mock_process.name.return_value = "test_process"

    with patch("psutil.net_connections", return_value=[mock_conn]):
        with patch("psutil.Process", return_value=mock_process):
            mapper = PortMapper([80])
            result = mapper.get_port_info()
            assert result == [{"port": 80, "pid": 123, "name": "test_process"}]
