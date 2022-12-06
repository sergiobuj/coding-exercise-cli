import json
from abc import ABC, abstractmethod
from io import IOBase


class OutputFormatter(ABC):
    """OutputFormatter defines the abstract class to derive any output "formatter" we
    want to implement.

    An output "formatter" determines the specifics of writing the output file.

    New implementations need to provide the file extension and write the `data` (Python dict)
    to the opened file.

    This class is not responsible for opening or creating a file. This writes the content to
    an object that supports writing to a byte stream.
    """

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
