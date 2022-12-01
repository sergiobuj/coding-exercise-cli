from abc import ABC, abstractmethod
from collections.abc import Generator
from io import BufferedReader

from .models import LogEntry


class LogReader(ABC):
    @abstractmethod
    def __init__(self, file: BufferedReader):
        "Constructor receives the opened file"

    @abstractmethod
    def logs(self) -> Generator[LogEntry, None, None]:
        "Support for an iterable of LogEntries"
