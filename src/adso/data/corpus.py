"Corpus Class and subclasses"

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union

import dask.array as da
import h5py


from .common import compute_hash


class Corpus(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.update_hash()

    @abstractmethod
    def get(self) -> Any:
        raise NotImplementedError

    def update_hash(self) -> None:
        self.hash = compute_hash(self.path)

    def serialize(self) -> Dict[str, str]:
        return {
            "format": type(self).__name__,
            "path": str(self.path),
            "hash": self.hash,
        }

    @classmethod
    def load(cls, path: Union[Path, str], hash: str) -> "Corpus":
        path = Path(path)
        if path.is_file():
            corpus = cls(path)
            if corpus.hash == hash:
                return corpus
            else:
                raise RuntimeError("Different hash")
        else:
            raise RuntimeError("File already exists")


class Raw(Corpus):
    def get(self) -> da.array:
        if self.hash == compute_hash(self.path):
            return da.from_array(h5py.File(self.path, "r")["/raw"])
        else:
            raise RuntimeError("Different hash")

    @classmethod
    def from_dask_array(cls, path: Path, array: da.array) -> "Raw":
        if path.is_file():
            raise RuntimeError("File already exists")
        else:
            array.to_hdf5(path, "/raw", shuffle=False)
        return Raw(path)
