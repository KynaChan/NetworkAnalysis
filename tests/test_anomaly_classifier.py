from unittest.mock import MagicMock

import pytest

from network_analyzer.anomaly_classifier import AnomalyClassifier


def test_init_sets_attributes():
    mock_model = MagicMock()
    anomalies = [[1, 2], [3, 4]]
    clf = AnomalyClassifier(mock_model, anomalies)
    assert clf.rf_model == mock_model
    assert clf.identified_anomalies == anomalies
    assert clf.rf_predictions is None


def test_classify_anomalies_calls_predict_and_returns_predictions():
    mock_model = MagicMock()
    anomalies = [[1, 2], [3, 4]]
    mock_model.predict.return_value = [0, 1]
    clf = AnomalyClassifier(mock_model, anomalies)
    preds = clf.classify_anomalies()
    mock_model.predict.assert_called_once_with(anomalies)
    assert preds == [0, 1]
    assert clf.rf_predictions == [0, 1]


def test_classify_anomalies_raises_if_model_is_none():
    anomalies = [[1, 2], [3, 4]]
    clf = AnomalyClassifier(None, anomalies)
    with pytest.raises(ValueError, match="Model not provided"):
        clf.classify_anomalies()
