import pickle

from dask_ml.feature_extraction.text import CountVectorizer

from .common import compute_hash
from .corpus import Corpus


class Vectorizer(Corpus):
    def get(self) -> CountVectorizer:
        if self.hash == compute_hash(self.path):
            return pickle.load(self.path.open("rb"))
        else:
            raise RuntimeError("Different hash")
