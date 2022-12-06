import re
import sys
from io import BufferedIOBase
from typing import Generator

from ..models import LogEntry
from .base import LogReaderBase


class SquidLogReader(LogReaderBase):
    """
    LogReader to parse the 'native' access.log file from Squid.
    Each log entry has the following components:

    time elapsed remotehost code/status bytes method URL rfc931 peerstatus/peerhost type

    TODO: Add support for the 'common' format.
        remotehost rfc931 authuser [date] "method URL" status bytes

        source: https://docstore.mik.ua/squid/FAQ-6.html
    """

    SQUID_NATIVE_FORMAT = r"""^
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

    def __init__(self, file: BufferedIOBase):
        self.entry_regex = re.compile(self.SQUID_NATIVE_FORMAT, re.VERBOSE)
        self.file = file

    def logs(self) -> Generator[LogEntry, None, None]:
        if not self.file:
            return

        log_line = self.file.readline()
        while log_line:
            search_obj = self.entry_regex.match(log_line.decode("utf-8"))
            if search_obj:
                yield LogEntry(**search_obj.groupdict())
            else:
                print(f"couldn't process {log_line}", file=sys.stderr)

            log_line = self.file.readline()
