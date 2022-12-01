from abc import ABC, abstractmethod
from collections import Counter
from datetime import datetime

from dateutil import tz

from .models import LogEntry


class Metrics(ABC):
    @abstractmethod
    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        "Update the metric with a new LogEntry value"

    @abstractmethod
    def report(self, *args, **kwargs) -> dict | str | int | float:
        "Return the value of the metric"


class IPCounter(Metrics):
    def __init__(self) -> None:
        self.counter = Counter()

    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        self.counter.update([log_entry.remotehost])
        return True

    def report(self, *args, **kwargs) -> dict | str | int | float:
        if not self.counter:
            return ""

        if "lfip" in kwargs:
            return self.counter.most_common()[-1][0]

        return self.counter.most_common(1)[0][0]


class BytesCounter(Metrics):
    def __init__(self) -> None:
        self.total_bytes = 0

    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        self.total_bytes += int(log_entry.bytes)
        return True

    def report(self, *args, **kwargs) -> dict | str | int | float:
        return self.total_bytes


class EventRate(Metrics):
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
