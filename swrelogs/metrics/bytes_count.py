from ..models import LogEntry
from .base import MetricBase


class BytesCounter(MetricBase):
    def __init__(self) -> None:
        self.total_bytes = 0

    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        self.total_bytes += max(int(log_entry.bytes), 0)
        return True

    def report(self, *args, **kwargs) -> dict | str | int | float:
        return self.total_bytes

    def label(self, *args, **kwargs) -> str:
        return "bytes"
