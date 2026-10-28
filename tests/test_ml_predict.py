import joblib
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from ml.predict import CategoryPredictor


@pytest.fixture
def model_path(tmp_path):
    model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    model.fit(
        ["pizza place", "burger bar", "bus ticket", "train ticket"],
        ["Food & Dining", "Food & Dining", "Transportation", "Transportation"],
    )
    path = tmp_path / "model.joblib"
    joblib.dump(model, path)
    return path


def test_suggest_returns_category_and_confidence(model_path):
    category, confidence = CategoryPredictor(model_path).suggest("pizza bar")

    assert category == "Food & Dining"
    assert 0.5 < confidence <= 1


def test_missing_model_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        CategoryPredictor(tmp_path / "missing.joblib").suggest("pizza")
