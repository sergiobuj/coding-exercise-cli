import re
from collections.abc import Generator

from .log_reader import LogReader
from .models import LogEntry


class SquidLogReader(LogReader):
    """time elapsed remotehost code/status bytes method URL rfc931 peerstatus/peerhost type"""

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

    def __init__(self, path: str):
        self.filepath = path
        self.entry_regex = re.compile(self.SQUID_LOGENTRY_FORMAT, re.VERBOSE)
        self.file = None

    def __enter__(self) -> "SquidLogReader":
        self.file = open(self.filepath, "rb")
        return self

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        if self.file:
            self.file.close()

    def logs(self) -> Generator[LogEntry, None, None]:
        if not self.file:
            return

        while log_line := self.file.readline():
            if search_obj := self.entry_regex.match(log_line.decode("utf-8")):
                yield LogEntry(**search_obj.groupdict())
            else:
                print(f"couldn't process {log_line}")
