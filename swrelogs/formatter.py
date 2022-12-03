import json
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


class JSONFormatter(OutputFormatter):
    def __init__(self, data: dict):
        self.data = data

    def write(self, file: IOBase) -> None:
        contents = json.dumps(self.data)
        file.write(contents)
