from ..models import LogEntry
from .base import MetricBase



class BytesCounter(MetricBase):
    def __init__(self) -> None:
        self.total_bytes = 0

    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        self.total_bytes += int(log_entry.bytes)
        return True

    def report(self, *args, **kwargs) -> dict | str | int | float:
        return self.total_bytes
