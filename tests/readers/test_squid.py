import io
import unittest

from swrelogs.models import LogEntry
from swrelogs.readers import SquidLogReader


class TestSquidLogReader(unittest.TestCase):
    def test_subclass(self):
        reader = SquidLogReader(io.BytesIO())
        self.assertTrue(hasattr(reader, "logs"))

    def test_parses_multiple_log_entry(self):
        sample_log = b"""
1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
1157689313 1000 10.10.10.19 TCP_MISS/200 1000 CONNECT example.com:443 users DIRECT/209.19.17.11 -
"""

        expected_logs = [
            LogEntry(
                timestamp=1157689312.049,
                elapsed=5006,
                remotehost="10.105.21.199",
                status="TCP_MISS/200",
                bytes=19763,
                method="CONNECT",
                url="login.yahoo.com:443",
                user="badeyek",
                peer="DIRECT/209.73.177.115",
                type="-",
            ),
            LogEntry(
                timestamp=1157689313,
                elapsed=1000,
                remotehost="10.10.10.19",
                status="TCP_MISS/200",
                bytes=1000,
                method="CONNECT",
                url="example.com:443",
                user="users",
                peer="DIRECT/209.19.17.11",
                type="-",
            ),
        ]

        reader = SquidLogReader(io.BytesIO(sample_log))
        log_entries = list(reader.logs())
        self.assertEqual(log_entries, expected_logs)

    def test_parser_ignored_invalid_log_entries(self):
        invalid_log_entries = [
            b"",
            b"\n\n\n\n\n",
            b"1157689312.049   5006 10.105.21.199 TCP_MISS/200 19 badeyek DIRECT/unprocessable entry",
            b'10.105.21.199 badeyek - "Wed, 4 Dec 2022 22:22:22 GMT" "GET example.com" 200 100',
        ]

        for log_entry in invalid_log_entries:
            reader = SquidLogReader(io.BytesIO(log_entry))
            logs = list(reader.logs())
            self.assertEqual(logs, [])
