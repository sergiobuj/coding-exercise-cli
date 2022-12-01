from abc import ABC, abstractmethod

from ..models import LogEntry


class MetricBase(ABC):
    @abstractmethod
    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        "Update the metric with a new LogEntry value"

    @abstractmethod
    def report(self, *args, **kwargs) -> dict | str | int | float:
        "Return the value of the metric"
