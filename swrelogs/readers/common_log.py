from datetime import datetime
import re
import sys
from io import BufferedIOBase
from typing import Generator

from ..models import LogEntry
from .base import LogReaderBase


class CommonLogReader(LogReaderBase):
    """
    remotehost rfc931 authuser [date] "method URL" status bytes
    """

    COMMON_FORMAT = r"""^
    (?P<remotehost>\S+)\s+
    (?P<user>\S+)\s+
    (?P<authuser>\S+)\s+
    \[(?P<date>.+)\]\s+
    \"(?P<method>\S+)\s+(?P<url>\S+)\s+(?P<httpver>\S+)\"\s+
    (?P<status>\S+)\s+
    (?P<bytes>\S+)$"""

    def __init__(self, file: BufferedIOBase):
        self.entry_regex = re.compile(self.COMMON_FORMAT, re.VERBOSE)
        self.file = file

    def logs(self) -> Generator[LogEntry, None, None]:
        if not self.file:
            return

        log_line = self.file.readline()
        while log_line:
            search_obj = self.entry_regex.match(log_line.decode("utf-8"))
            if search_obj:
                log_entry = search_obj.groupdict()
                try:
                    ttt = datetime.strptime(search_obj['date'], '%d/%b/%Y:%H:%M:%S %z')
                    log_entry["timestamp"] = ttt.timestamp()
                except ValueError:
                    # error parsing log date
                    log_entry["timestamp"] = 0

                yield LogEntry(**log_entry)
            else:
                print(f"couldn't process {log_line}", file=sys.stderr)

            log_line = self.file.readline()
