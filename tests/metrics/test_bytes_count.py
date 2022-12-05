import unittest

from swrelogs.metrics import BytesCounter
from swrelogs.models import LogEntry


class TestBytesCounter(unittest.TestCase):
    def test_subclass(self):
        counter = BytesCounter()
        self.assertTrue(hasattr(counter, "label"))
        self.assertTrue(hasattr(counter, "report"))
        self.assertTrue(hasattr(counter, "update"))


class TestBytesCountMetric(unittest.TestCase):
    def setUp(self):
        self.counter = BytesCounter()

    def test_empty_counter(self):
        self.assertEqual(0, self.counter.report())

    def test_bytes_count(self):
        self.counter.update(LogEntry(bytes=10))
        self.counter.update(LogEntry(bytes=20))

        self.assertEqual(30, self.counter.report(), "reports bytes sum")

    def test_ignore_negative_datapoints(self):
        self.counter.update(LogEntry(bytes=-10))
        self.counter.update(LogEntry(bytes=1))

        self.assertEqual(1, self.counter.report(), "reports bytes sum")


if __name__ == "__main__":
    unittest.main()
