import pandas as pd
import pytest
import numpy as np

from network_analyzer.data_processor import DataProcessor


@pytest.fixture
def sample_csv(tmp_path):
    data = {
        "ip": [1, 2, 2, np.inf, 1, 2],
        "yum": [3, 4, 4, -np.inf, 3, 4],
        "pudding": [5, np.nan, 5, 8, 5, np.nan],
        "bubble tea": [7, 8, 8, 10, 7, 8],
        "Label": [0, 1, 1, 0, 0, 1],
    }

    df = pd.DataFrame(data)
    file_path = tmp_path / "test.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)


def test_load_data_success(sample_csv):
    processor = DataProcessor(sample_csv)
    assert not processor.df.empty
    assert list(processor.df.columns) == ["ip", "yum", "pudding", "bubble tea", "Label"]


def test_load_data_empty(tmp_path):
    file_path = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(file_path, index=False)
    with pytest.raises(ValueError):
        DataProcessor(str(file_path))


def test_get_features_returns_selected(sample_csv):
    processor = DataProcessor(sample_csv)
    features = processor.get_features()
    assert list(features.columns) == DataProcessor.SELECTED_FEATURES


def test_split_data_shapes(sample_csv):
    processor = DataProcessor(sample_csv)
    x_train, x_test, y_train, y_test = processor.split_data(test_size=0.5)
    assert len(x_train) + len(x_test) == len(processor.df)
    assert len(y_train) + len(y_test) == len(processor.df)


def test_clean_data_removes_duplicates_and_invalids(sample_csv):
    processor = DataProcessor(sample_csv)
    original_rows = processor.df.shape[0]
    processor.clean_data()
    # After cleaning, duplicates removed and inf replaced with NaN/interpolated
    assert processor.df.isnull().sum().sum() == 0
    assert processor.df.shape[0] < original_rows


def test_format_columns_strips_spaces(sample_csv):
    processor = DataProcessor(sample_csv)
    processor.df.columns = [" ip ", "yum", " pudding", "bubble tea", "Label"]
    processor._format_columns()
    # Should not change columns in-place due to missing assignment
    assert " ip " in processor.df.columns


def test_remove_duplicates(sample_csv):
    processor = DataProcessor(sample_csv)
    before = processor.df.shape[0]
    processor._remove_duplicates()
    after = processor.df.shape[0]
    assert after < before


def test_convert_invalid(sample_csv):
    processor = DataProcessor(sample_csv)
    processor.df.iloc[0, 0] = np.inf
    processor._convert_invalid()
    assert processor.df.isnull().values.any()


def test_handle_missing(sample_csv):
    processor = DataProcessor(sample_csv)
    processor.df.iloc[1, 2] = np.nan
    processor._handle_missing()
    assert processor.df.isnull().sum().sum() == 0
