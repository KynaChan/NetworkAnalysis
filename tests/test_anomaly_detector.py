import pytest
from network_analyser.anomaly_detector import AnomalyDetector
import pandas as pd
from sklearn.ensemble import IsolationForest


@pytest.fixture
def sample_data():
    # Create a simple DataFrame with clear outliers
    data = pd.DataFrame({"feature1": [1, 2, 3, 100], "feature2": [1, 2, 3, -100]})
    return data


@pytest.fixture
def isolation_forest_model():
    # Return a fitted IsolationForest model
    def _fit_model(data):
        model = IsolationForest(random_state=42)
        model.fit(data)
        return model

    return _fit_model


def test_identify_anomalies_sets_attributes(sample_data, isolation_forest_model):
    model = isolation_forest_model(sample_data)
    detector = AnomalyDetector(model, sample_data)
    detector.if_identify_anomalies()
    assert detector.if_predictions is not None
    assert detector.anomalies is not None
    assert detector.benign is not None
    # Check that anomalies and benign are disjoint
    assert set(detector.anomalies.index).isdisjoint(detector.benign.index)


def test_transform_predictions_returns_correct_mapping(
    sample_data, isolation_forest_model
):
    model = isolation_forest_model(sample_data)
    detector = AnomalyDetector(model, sample_data)
    detector.if_identify_anomalies()
    transformed = detector.transform_predictions()
    # Should only contain 0 (benign) and 1 (anomaly)
    assert set(transformed.unique()).issubset({0, 1})
    # Check length matches input
    assert len(transformed) == len(sample_data)


def test_transform_predictions_raises_if_no_predictions(
    sample_data, isolation_forest_model
):
    model = isolation_forest_model(sample_data)
    detector = AnomalyDetector(model, sample_data)
    with pytest.raises(ValueError):
        detector.transform_predictions()
