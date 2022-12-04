import json
from abc import ABC, abstractmethod
from io import IOBase


class OutputFormatter(ABC):
    @abstractmethod
    def write(self, file: IOBase) -> None:
        "write the report"

    @abstractmethod
    def file_extension(self) -> str:
        "return the appropiate filepath with extension"


class JSONFormatter(OutputFormatter):
    def __init__(self, data: dict):
        self.data = data

    def file_extension(self) -> str:
        return "json"

    def write(self, file: IOBase) -> None:
        contents = json.dumps(self.data)
        file.write(contents)
