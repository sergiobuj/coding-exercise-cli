from abc import ABC, abstractmethod
from io import IOBase
from pathlib import Path


class OutputFormatter(ABC):
    @abstractmethod
    def write(self, file: IOBase) -> None:
        "write the report"

    @abstractmethod
    def get_path(self, filepath: str) -> Path:
        "return the appropiate filepath with extension"

