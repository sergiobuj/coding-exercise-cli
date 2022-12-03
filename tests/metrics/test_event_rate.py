from time import time
import unittest
from swrelogs.models import LogEntry
from swrelogs.metrics import EventRate


class TestEventRateCounter(unittest.TestCase):
    def test_subclass(self):
        counter = EventRate()
        self.assertTrue(hasattr(counter, "label"))
        self.assertTrue(hasattr(counter, "report"))
        self.assertTrue(hasattr(counter, "update"))


class TestEventRateMetric(unittest.TestCase):
    def setUp(self):
        self.counter = EventRate()

    def test_empty_counter(self):
        self.assertEqual(0, self.counter.report())

    def test_event_rate_count(self):
        t = time()
        self.counter.update(LogEntry(timestamp=t))
        self.counter.update(LogEntry(timestamp=t + 1))
        self.counter.update(LogEntry(timestamp=t + 2))

        self.assertEqual(1, self.counter.report(), "count 1 request per second")

    def test_event_rate_burst(self):
        t = time()
        self.counter.update(LogEntry(timestamp=t))
        self.counter.update(LogEntry(timestamp=t))
        self.counter.update(LogEntry(timestamp=t))
        self.counter.update(LogEntry(timestamp=t))

        self.assertEqual(4, self.counter.report(), "count burst requests")

    def test_sparse_events(self):
        t = time()
        self.counter.update(LogEntry(timestamp=t))
        self.counter.update(LogEntry(timestamp=t + 20))

        self.assertEqual(0.1, self.counter.report(), "count 1 request per second")


if __name__ == "__main__":
    unittest.main()
