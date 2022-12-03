import unittest
from swrelogs.models import LogEntry
from swrelogs.metrics import IPCounter


class TestIPCounter(unittest.TestCase):
    def test_subclass(self):
        counter = IPCounter()
        self.assertTrue(hasattr(counter, "label"))
        self.assertTrue(hasattr(counter, "report"))
        self.assertTrue(hasattr(counter, "update"))


class TestIPCountMetricMostFrequent(unittest.TestCase):
    def setUp(self):
        self.counter = IPCounter()

    def test_empty_counter(self):
        self.assertEqual("", self.counter.report())

    def test_ip_count(self):
        frequent_ip = "10.10.10.10"
        least_freq_ip = "10.10.10.11"

        self.counter.update(LogEntry(remotehost=least_freq_ip))
        self.counter.update(LogEntry(remotehost=frequent_ip))
        self.counter.update(LogEntry(remotehost=frequent_ip))

        self.assertEqual(frequent_ip, self.counter.report(), "reports most frequent IP")

    def test_only_one_ip(self):
        ip = "127.0.0.1"

        self.counter.update(LogEntry(remotehost=ip))
        self.counter.update(LogEntry(remotehost=ip))
        self.counter.update(LogEntry(remotehost=ip))
        self.counter.update(LogEntry(remotehost=ip))

        self.assertEqual(ip, self.counter.report(), "reports most frequent IP")


class TestIPCountMetricLeastFrequent(unittest.TestCase):
    def setUp(self):
        self.counter = IPCounter(least_frequent=True)

    def test_empty_counter(self):
        self.assertEqual("", self.counter.report())

    def test_ip_count(self):
        frequent_ip = "10.10.10.10"
        least_freq_ip = "10.10.10.11"

        self.counter.update(LogEntry(remotehost=least_freq_ip))
        self.counter.update(LogEntry(remotehost=frequent_ip))
        self.counter.update(LogEntry(remotehost=frequent_ip))

        self.assertEqual(
            least_freq_ip, self.counter.report(), "reports least frequent IP"
        )

    def test_only_one_ip(self):
        ip = "127.0.0.1"

        self.counter.update(LogEntry(remotehost=ip))
        self.counter.update(LogEntry(remotehost=ip))
        self.counter.update(LogEntry(remotehost=ip))
        self.counter.update(LogEntry(remotehost=ip))

        self.assertEqual(ip, self.counter.report(), "reports least frequent IP")


if __name__ == "__main__":
    unittest.main()
