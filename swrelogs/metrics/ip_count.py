from collections import Counter

from ..models import LogEntry
from .base import MetricBase


class IPCounter(MetricBase):
    def __init__(self, least_frequent: bool = False) -> None:
        self.counter = Counter()
        self.least_frequent = least_frequent

    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        self.counter.update([log_entry.remotehost])
        return True

    def report(self, *args, **kwargs) -> dict | str | int | float:
        if not self.counter:
            return ""

        if self.least_frequent:
            return self.counter.most_common()[-1][0]

        return self.counter.most_common(1)[0][0]

    def label(self) -> str:
        return "lfip" if self.least_frequent else "mfip"
