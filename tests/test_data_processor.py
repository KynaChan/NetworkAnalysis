import os
import tempfile

import pandas as pd
import pytest

from network_analyzer.data_processor import DataProcessor


@pytest.fixture
def sample_csv(tmp_path):
    data = {
        "ip": [1, 2, 2, 4],
        "yum": [10, 20, 20, 40],
        "pudding": [100, 200, 200, 400],
        "bubble tea": [1000, 2000, 2000, 4000],
        "Label": [0, 1, 1, 0],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)


def test_init_raises_on_empty_csv(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(empty_csv, index=False)
    with pytest.raises(ValueError):
        DataProcessor(str(empty_csv))


def test_select_features(sample_csv):
    dp = DataProcessor(sample_csv)
    dp.select_features()
    assert set(dp.features.columns) == {"ip", "yum", "pudding", "bubble tea"}


def test_remove_duplicates(sample_csv):
    dp = DataProcessor(sample_csv)
    dp.select_features()
    dp.remove_duplicates()
    assert len(dp.features) == 3  # 3 unique rows


def test_convert_invalid(sample_csv):
    dp = DataProcessor(sample_csv)
    dp.select_features()
    dp.features.iloc[0, 0] = float("inf")
    dp.convert_invalid()
    assert pd.isna(dp.features.iloc[0, 0])


def test_handle_missing(sample_csv):
    dp = DataProcessor(sample_csv)
    dp.select_features()
    dp.features.iloc[1, 1] = None
    dp.handle_missing()
    assert not pd.isna(dp.features.iloc[1, 1]) 


def test_drop_label(sample_csv):
    dp = DataProcessor(sample_csv)
    dp.select_features()
    dp.features["Label"] = [0, 1, 0, 1]
    dp.drop_label()
    assert "Label" not in dp.features.columns
    assert dp.labels is not None


def test_split_data(sample_csv):
    dp = DataProcessor(sample_csv)
    dp.process_data()
    x_train, x_test, y_train, y_test = dp.split_data()
    assert len(x_train) + len(x_test) == len(dp.features) + len(
        x_test
    )  # x_test is not dropped from features
    assert len(y_train) + len(y_test) == len(dp.labels)


def test_process_supervised_data(sample_csv):
    dp = DataProcessor(sample_csv)
    x_train, x_test, y_train, y_test = dp.process_rf_data()
    assert all(len(arr) > 0 for arr in [x_train, x_test, y_train, y_test])
