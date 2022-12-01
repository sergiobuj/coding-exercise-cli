from abc import ABC, abstractmethod
from collections.abc import Generator

from .models import LogEntry


class LogReader(ABC):
    @abstractmethod
    def logs(self) -> Generator[LogEntry, None, None]:
        "support for an iterable of LogEntries"

    @abstractmethod
    def __enter__(self):
        "support for context manager"

    @abstractmethod
    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        "support for context manager"
