"""Python tool to analyze squid logs."""
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime

from dateutil import tz

SQUID_LOGENTRY_FORMAT = r"""^
(?P<timestamp>\S+)\s+
(?P<elapsed>\d+)\s+
(?P<remotehost>\S+)\s+
(?P<status>\S+)\s+
(?P<bytes>\S+)\s+
(?P<method>\S+)\s+
(?P<url>\S+)\s+
(?P<user>\S+)\s+
(?P<peer>\S+)\s+
(?P<type>\S+)$"""

squid_regex = re.compile(SQUID_LOGENTRY_FORMAT, re.VERBOSE)

# pylint: disable=R0902
@dataclass
class LogEntry:
    """time elapsed remotehost code/status bytes method URL rfc931 peerstatus/peerhost type"""
    timestamp: float = 0
    elapsed: int = 0
    remotehost: str = ""
    status: str = ""
    bytes: int = 0
    method: str = ""
    url: str = ""
    user: str = ""
    peer: str = ""
    type: str = ""


def analyze_logs(filepath: str) -> dict[str, float | int | str]:
    """Retrieve insights from squid logs"""
    bytes_total = 0
    ip_counter = Counter()
    log_entries_count = 0
    min_timestamp, max_timestamp = float("Inf"), float("-Inf")

    with open(filepath, "rb") as log:
        while log_line := log.readline():
            if search_obj := squid_regex.match(log_line.decode("utf-8")):
                entry = LogEntry(**search_obj.groupdict())

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


if __name__ == "__main__":
    FILEPATH = "./sample_data/access.log"
    result = analyze_logs(FILEPATH)
    print(result)
