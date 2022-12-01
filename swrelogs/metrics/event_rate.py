from datetime import datetime

from dateutil import tz

from ..models import LogEntry
from .base import MetricBase


class EventRate(MetricBase):
    def __init__(self) -> None:
        self.entries_count = 0
        self.min_timestamp = float("Inf")
        self.max_timestamp = float("-Inf")

    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        self.entries_count += 1
        self.min_timestamp = min(self.min_timestamp, float(log_entry.timestamp))
        self.max_timestamp = max(self.max_timestamp, float(log_entry.timestamp))
        return True

    def report(self, *args, **kwargs) -> dict | str | int | float:
        min_datetime = datetime.fromtimestamp(self.min_timestamp, tz=tz.UTC)
        max_datetime = datetime.fromtimestamp(self.max_timestamp, tz=tz.UTC)
        diff_datetime = max_datetime - min_datetime

        return self.entries_count / diff_datetime.total_seconds()
