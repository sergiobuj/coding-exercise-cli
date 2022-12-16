from io import IOBase
from typing import List, Type

from .metrics import MetricBase
from .readers import LogReaderBase, SquidLogReader, CommonLogReader


def _get_log_reader(file: IOBase) -> Type[LogReaderBase]:
    # Determine log file format, only one for now.
    if file.name.endswith(".common.log"):
        return CommonLogReader
    return SquidLogReader


def run_log_analyzer(source_filepath: str, metrics: List[MetricBase]) -> None:
    try:
        with open(source_filepath, "rb") as file:
            reader = _get_log_reader(file)
            for entry in reader(file).logs():
                for metric in metrics:
                    metric.update(entry)
    except IsADirectoryError as e:
        # Log error
        pass
