import unittest
from unittest import mock

from swrelogs import run_log_analyzer
from swrelogs.metrics import BytesCounter, IPCounter

SAMPLE_VALID_LOG = b"""
1157689313 1 10.105.21.199 TCP_MISS/200 5000 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
1157689313 1 10.10.10.19 TCP_MISS/200 1000 CONNECT example.com:443 users DIRECT/209.19.17.11 -
"""


class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.log_file_mock = mock.mock_open(read_data=SAMPLE_VALID_LOG)

    @mock.patch("os.path.isfile")
    def test_log_analyzer_runner(self, isfile_mock):
        isfile_mock.return_value = True

        bytes_metric = BytesCounter()
        ip_metric = IPCounter()

        with mock.patch("swrelogs.log_analyzer.open", self.log_file_mock):
            run_log_analyzer("./fake_filepath", [bytes_metric, ip_metric])

        self.assertEqual(bytes_metric.report(), 6000)
        self.assertEqual(ip_metric.report(), "10.105.21.199")
