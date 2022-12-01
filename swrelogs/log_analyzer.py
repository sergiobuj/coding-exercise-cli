from io import BufferedReader

from dateutil import tz

from .metrics import BytesCounter, EventRate, IPCounter
from .readers.squid import SquidLogReader


def _get_log_reader(file: BufferedReader):
    # Determine log file format, only one for now.
    return SquidLogReader


def log_analyzer(
    source_filepath: str, *args, **kwargs
) -> dict[str, dict | float | int | str]:
    event_rate_metric = EventRate()
    ip_count_metric = IPCounter()
    total_bytes_metric = BytesCounter()

    metrics = [event_rate_metric, ip_count_metric, total_bytes_metric]

    with open(source_filepath, "rb") as file:
        reader = _get_log_reader(file)
        for entry in reader(file).logs():
            for metric in metrics:
                metric.update(entry)

    return {
        "mfip": ip_count_metric.report(),
        "lfip": ip_count_metric.report(lfip=True),
        "eps": event_rate_metric.report(),
        "bytes": total_bytes_metric.report(),
    }
