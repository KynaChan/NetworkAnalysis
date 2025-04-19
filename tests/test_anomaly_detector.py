import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

from network_analyzer.anomaly_detector import AnomalyDetector


def test_anomalydetector_run_returns_transformed_predictions():
    # Arrange
    data = pd.DataFrame({"a": [0, 0, 100, 0]})
    model = IsolationForest(random_state=42).fit(data)
    detector = AnomalyDetector(model, data)

    # Act
    result = detector.run()

    # Assert
    assert isinstance(result, pd.Series)
    assert set(result.unique()).issubset({0, 1})


def test_identify_anomalies_sets_attributes():
    data = pd.DataFrame({"a": [1, 2, 100, 2]})
    model = IsolationForest(random_state=0).fit(data)
    detector = AnomalyDetector(model, data)
    detector.identify_anomalies()

    assert detector.if_predictions is not None
    assert detector.anomalies is not None
    assert detector.benign is not None


def test_transform_predictions_raises_without_predictions():
    detector = AnomalyDetector(None, None)
    with pytest.raises(ValueError):
        detector.transform_predictions()


def test_identify_anomalies_raises_without_model_or_data():
    detector = AnomalyDetector(None, None)
    with pytest.raises(ValueError):
        detector.identify_anomalies()


def test_extract_anomalies_returns_anomalies():
    data = pd.DataFrame({"a": [1, 2, 100, 2]})
    model = IsolationForest(random_state=0).fit(data)
    detector = AnomalyDetector(model, data)
    detector.identify_anomalies()
    anomalies = detector.extract_anomalies()
    assert isinstance(anomalies, pd.DataFrame)
