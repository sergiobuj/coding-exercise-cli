from io import IOBase
from typing import List

from .metrics import MetricBase
from .readers.squid import SquidLogReader


def _get_log_reader(file: IOBase):
    # Determine log file format, only one for now.
    return SquidLogReader


def log_analyzer(source_filepath: str, metrics: List[MetricBase]) -> None:
    with open(source_filepath, "rb") as file:
        reader = _get_log_reader(file)
        for entry in reader(file).logs():
            for metric in metrics:
                metric.update(entry)
