from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from network_analyzer.network_sniffer import NetworkSniffer


def test_init_sets_attributes():
    sniffer = NetworkSniffer(interface="lo", count=10)
    assert sniffer.interface == "lo"
    assert sniffer.count == 10
    assert sniffer.output_df is None


@patch("network_analyzer.network_sniffer.NetworkSniffer.capture_traffic")
@patch("network_analyzer.network_sniffer.NetworkSniffer.transform_traffic_data")
def test_run_calls_capture_and_transform(mock_transform, mock_capture):
    sniffer = NetworkSniffer()
    sniffer.output_df = pd.DataFrame({"a": [1]})
    result = sniffer.run()
    mock_capture.assert_called_once()
    mock_transform.assert_called_once()
    assert result.equals(pd.DataFrame({"a": [1]}))


@patch("subprocess.run")
@patch("os.path.exists", return_value=True)
def test_capture_traffic_creates_file(mock_exists, mock_run):
    sniffer = NetworkSniffer()
    sniffer.capture_traffic()
    mock_run.assert_called_once()
    mock_exists.assert_called_with("sniffed_traffic.pcap")


@patch("subprocess.run")
@patch("os.path.exists", return_value=False)
def test_capture_traffic_raises_if_file_not_created(mock_exists, mock_run):
    sniffer = NetworkSniffer()
    with pytest.raises(FileNotFoundError):
        sniffer.capture_traffic()


@patch("subprocess.run")
@patch("os.path.exists", return_value=True)
@patch("pandas.read_csv")
def test_transform_traffic_data_success(mock_read_csv, mock_exists, mock_run):
    sniffer = NetworkSniffer()
    sniffer.pcap_file_path = "sniffed_traffic.pcap"
    mock_read_csv.return_value = pd.DataFrame({"col": [1]})
    sniffer.transform_traffic_data("output.csv")
    mock_run.assert_called_once()
    mock_exists.assert_called_with("output.csv")
    assert isinstance(sniffer.df, pd.DataFrame)


@patch("subprocess.run")
@patch("os.path.exists", return_value=True)
@patch("pandas.read_csv")
def test_transform_traffic_data_empty_df_raises(mock_read_csv, mock_exists, mock_run):
    sniffer = NetworkSniffer()
    sniffer.pcap_file_path = "sniffed_traffic.pcap"
    mock_read_csv.return_value = pd.DataFrame()
    with pytest.raises(ValueError):
        sniffer.transform_traffic_data("output.csv")
