import re
from collections.abc import Generator
from io import BufferedReader

from .log_reader_base import LogReader
from ..models import LogEntry


class SquidLogReader(LogReader):
    """
    LogReader to parse the access.log file from Squid.
    Each log entry has the following components:

    time elapsed remotehost code/status bytes method URL rfc931 peerstatus/peerhost type
    """

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

    def __init__(self, file: BufferedReader):
        self.entry_regex = re.compile(self.SQUID_LOGENTRY_FORMAT, re.VERBOSE)
        self.file = file

    def logs(self) -> Generator[LogEntry, None, None]:
        if not self.file:
            return

        while log_line := self.file.readline():
            if search_obj := self.entry_regex.match(log_line.decode("utf-8")):
                yield LogEntry(**search_obj.groupdict())
            else:
                print(f"couldn't process {log_line}")
