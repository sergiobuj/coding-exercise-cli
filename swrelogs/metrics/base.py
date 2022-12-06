from abc import ABC, abstractmethod
from typing import Union

from ..models import LogEntry


class MetricBase(ABC):
    @abstractmethod
    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        "Update the metric with a new LogEntry value"

    @abstractmethod
    def report(self, *args, **kwargs) -> Union[str, int, float]:
        "Return the value of the metric"

    @abstractmethod
    def label(self, *args, **kwargs) -> str:
        "Return the label of the metric"
