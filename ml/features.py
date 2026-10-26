"""Feature transformers for the transaction categoriser."""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class SentenceEmbedder(BaseEstimator, TransformerMixin):
    """Turn texts into sentence embeddings with a pretrained SentenceTransformer."""

    def __init__(self, model_name="all-MiniLM-L6-v2", batch_size=256):
        self.model_name = model_name
        self.batch_size = batch_size

    def _get_encoder(self):
        # Load the model on first use (also after joblib.load, since it is not pickled)
        if getattr(self, "_encoder", None) is None:
            from sentence_transformers import SentenceTransformer
            self._encoder = SentenceTransformer(self.model_name)
        return self._encoder

    def fit(self, X, y=None):
        # Pretrained model: nothing to learn
        return self

    def transform(self, X):
        texts = list(X)
        unique = pd.unique(pd.Series(texts))
        emb = self._get_encoder().encode(list(unique), batch_size=self.batch_size)
        lookup = dict(zip(unique, emb))
        return np.vstack([lookup[t] for t in texts])

    def __getstate__(self):
        # Keep the PyTorch model out of the pickle; _get_encoder reloads it
        state = super().__getstate__().copy()
        state.pop("_encoder", None)
        return state
