import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

from anomaly_detector.anomaly_detector import AnomalyDetector


@pytest.fixture()
def test_data():
    # 10 normal points, 2 outliers
    normal_data = np.random.normal(0, 1, (10, 2))
    outlier_data = np.random.normal(10, 1, (2, 2))
    data = np.vstack([normal_data, outlier_data])
    return pd.DataFrame(data, columns=["feature1", "feature2"])


def test_identify_anomalies_success(test_data):
    data = test_data
    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(data)

    detector = AnomalyDetector(model=model, processed_data=data)
    anomalies = detector.identify_anomalies()

    assert anomalies is not None
    assert isinstance(anomalies, pd.DataFrame)
    assert len(anomalies) > 0
    assert len(detector.benign) > 0


def test_identify_anomalies_failure():
    detector = AnomalyDetector()
    with pytest.raises(ValueError, match=r".*Model or processed data.*"):
        detector.identify_anomalies()


def test_save_anomalies(tmp_path, test_data):
    # Setup
    data = test_data
    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(data)

    detector = AnomalyDetector(model=model, processed_data=data)
    detector.identify_anomalies()

    output_file = tmp_path / "anomalies.csv"
    detector.save_anomalies(output_file=str(output_file))

    # Assert file is created and not empty
    assert output_file.exists()
    saved_data = pd.read_csv(output_file)
    assert not saved_data.empty


def test_save_anomalies_without_identification():
    detector = AnomalyDetector()
    with pytest.raises(ValueError, match=r".*No anomalies to save.*"):
        detector.save_anomalies("dummy.csv")
