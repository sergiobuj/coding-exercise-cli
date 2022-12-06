from abc import ABC, abstractmethod
from io import BufferedIOBase
from typing import Generator

from ..models import LogEntry


class LogReaderBase(ABC):
    @abstractmethod
    def __init__(self, file: BufferedIOBase):
        "Constructor receives the opened file"

    @abstractmethod
    def logs(self) -> Generator[LogEntry, None, None]:
        "Support for an iterable of LogEntries"
