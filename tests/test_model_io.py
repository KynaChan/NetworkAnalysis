from unittest import mock
from network_analyser.model_io import ModelIO
import joblib


class DummyModel:
    def __init__(self, value):
        self.value = value


def test_save_model_success(tmp_path):
    model = DummyModel(42)
    file_path = tmp_path / "model.pkl"
    model_io = ModelIO()
    model_io.save_model(model, str(file_path))
    assert file_path.exists()


def test_save_model_file_not_found(monkeypatch):
    model_io = ModelIO()
    model = DummyModel(1)
    with mock.patch("joblib.dump", side_effect=FileNotFoundError):
        model_io.save_model(model, "/invalid/path/model.pkl")


def test_save_model_general_exception(monkeypatch):
    model_io = ModelIO()
    model = DummyModel(1)
    with mock.patch("joblib.dump", side_effect=Exception("Some error")):
        model_io.save_model(model, "/some/path/model.pkl")


def test_load_model_success(tmp_path):
    model = DummyModel(99)
    file_path = tmp_path / "model.pkl"
    joblib.dump(model, file_path)
    model_io = ModelIO()
    loaded_model = model_io.load_model(str(file_path))
    assert isinstance(loaded_model, DummyModel)
    assert loaded_model.value == 99


def test_load_model_file_not_found():
    model_io = ModelIO()
    result = model_io.load_model("/non/existent/file.pkl")
    assert result is None


def test_load_model_general_exception(monkeypatch):
    model_io = ModelIO()
    with mock.patch("joblib.load", side_effect=Exception("Load error")):
        result = model_io.load_model("/some/path/model.pkl")
        assert result is None
