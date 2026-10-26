"""Load the saved category model and suggest a category for a description."""

from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "category_model.joblib"


class CategoryPredictor:
    """Suggest a transaction category with the saved model."""

    def __init__(self, model_path=MODEL_PATH):
        self.model_path = Path(model_path)
        self._model = None

    def _get_model(self):
        # Load once, on first use: loading takes a few seconds
        if self._model is None:
            self._model = joblib.load(self.model_path)
        return self._model

    def suggest(self, description: str) -> tuple[str, float]:
        model = self._get_model()
        proba = model.predict_proba([description])[0]
        best = proba.argmax()
        return str(model.classes_[best]), float(proba[best])
