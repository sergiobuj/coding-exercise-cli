import io
import unittest

from swrelogs.formatter import JSONFormatter


class TestJSONFormatter(unittest.TestCase):
    def test_subclass(self):
        formatter = JSONFormatter({})
        self.assertTrue(hasattr(formatter, "file_extension"))
        self.assertTrue(hasattr(formatter, "write"))

    def test_file_extension(self):
        formatter = JSONFormatter({})
        self.assertEqual(formatter.file_extension(), "json")

    def test_writes_valid_json(self):
        data = {"bytes": 1000}
        formatter = JSONFormatter(data)
        with io.StringIO() as file:
            formatter.write(file)
            self.assertEqual(file.getvalue(), '{"bytes": 1000}')
