from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from network_analyzer.network_sniffer import NetworkSniffer

@pytest.fixture
def network_sniffer():
    return NetworkSniffer(interface='test0', count=10)

def test_init():
    sniffer = NetworkSniffer('test0', 50)
    assert sniffer.interface == 'test0'
    assert sniffer.count == 50
    assert sniffer.output_df is None

@pytest.mark.integration
def test_capture_traffic(network_sniffer):
    with patch('subprocess.run') as mock_run:
        network_sniffer.capture_traffic()
        mock_run.assert_called_once_with([
            'tcpdump', '-i', 'test0', 
            '-c', '10', '-w', 'sniffed_traffic.pcap'
        ])

def test_capture_traffic_file_not_found(network_sniffer):
    with patch('subprocess.run'), \
         patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            network_sniffer.capture_traffic()

def test_transform_traffic_data(network_sniffer):
    test_df = pd.DataFrame({'col1': [1,2], 'col2': [3,4]})
    
    with patch('subprocess.run'), \
         patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=test_df):
        network_sniffer.transform_traffic_data()
        assert network_sniffer.df.equals(test_df)

def test_transform_traffic_empty_df(network_sniffer):
    with patch('subprocess.run'), \
         patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=pd.DataFrame()):
        with pytest.raises(ValueError):
            network_sniffer.transform_traffic_data()

def test_transform_traffic_file_not_found(network_sniffer):
    with patch('subprocess.run'), \
         patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            network_sniffer.transform_traffic_data()

def test_run_success(network_sniffer):
    test_df = pd.DataFrame({'col1': [1,2], 'col2': [3,4]})
    with patch.object(network_sniffer, 'capture_traffic'), \
         patch.object(network_sniffer, 'transform_traffic_data'):
        network_sniffer.output_df = test_df
        result = network_sniffer.run()
        assert result.equals(test_df)

def test_run_exception(network_sniffer):
    with patch.object(network_sniffer, 'capture_traffic', 
                     side_effect=Exception('Test error')):
        with pytest.raises(Exception) as exc:
            network_sniffer.run()
        assert 'Test error' in str(exc.value)
