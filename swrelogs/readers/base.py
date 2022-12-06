from abc import ABC, abstractmethod
from io import BufferedIOBase
from typing import Generator

from ..models import LogEntry


class LogReaderBase(ABC):
    """LogReaderBase defines the abstract class to derive the different log file parsers we
    want to implement.

    The log file readers will behave as a generator and will `yield` an instance of
    the LogEntry dataclass for each log line it parsers.
    """

    @abstractmethod
    def __init__(self, file: BufferedIOBase):
        "Constructor receives the opened file"

    @abstractmethod
    def logs(self) -> Generator[LogEntry, None, None]:
        "Support for an iterable of LogEntries"
