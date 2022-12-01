from collections import Counter
from datetime import datetime

from dateutil import tz

from .log_reader import LogReader


def log_analyzer(log_reader: LogReader) -> dict[str, float | int | str]:
    bytes_total = 0
    ip_counter = Counter()
    log_entries_count = 0
    min_timestamp, max_timestamp = float("Inf"), float("-Inf")

    with log_reader as reader:
        for entry in reader.logs():
            log_entries_count += 1
            ip_counter.update([entry.remotehost])
            bytes_total += int(entry.bytes)
            min_timestamp = min(min_timestamp, float(entry.timestamp))
            max_timestamp = max(max_timestamp, float(entry.timestamp))


    min_datetime = datetime.fromtimestamp(min_timestamp, tz=tz.UTC)
    max_datetime = datetime.fromtimestamp(max_timestamp, tz=tz.UTC)
    diff_datetime = max_datetime - min_datetime
    return {
        "mfip": ip_counter.most_common(1)[0][0],
        "lfip": ip_counter.most_common()[-1][0],
        "eps": log_entries_count / diff_datetime.total_seconds(),
        "bytes": bytes_total,
    }
