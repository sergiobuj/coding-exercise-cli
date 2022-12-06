from abc import ABC, abstractmethod
from typing import Union

from ..models import LogEntry


class MetricBase(ABC):
    """MetricBase defines the abstract class to derive the metric collector we want to implement.

    For each log line, our metric collector will receive an update method call with an instance of
    the LogEntry dataclass as the parameter.

    The report method should return the current value of the metric and the label is the title we
    will use in the report for this metric.

    This abstract class intends to define metric collectors that produce a
    single value.
    """

    @abstractmethod
    def update(self, log_entry: LogEntry, *args, **kwargs) -> bool:
        "Update the metric with a new LogEntry value"

    @abstractmethod
    def report(self, *args, **kwargs) -> Union[str, int, float]:
        "Return the value of the metric"

    @abstractmethod
    def label(self, *args, **kwargs) -> str:
        "Return the label of the metric"
