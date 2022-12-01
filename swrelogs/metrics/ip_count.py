from collections import Counter

from ..models import LogEntry
from .base import MetricBase

class IPCounter(MetricBase):
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
