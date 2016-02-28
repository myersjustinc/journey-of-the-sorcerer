from pathlib import Path
import unittest

from journey.reader.archive import Archive


class ArchiveTestCase(unittest.TestCase):
    def setUp(self):
        self.fixtures_path = Path(__file__).parent / 'fixtures'
        self.archive_path = self.fixtures_path / 'export.zip'
        self.archive = Archive(self.archive_path)

    def test_zip_loaded(self):
        self.assertTrue(
            hasattr(self.archive, '_zip'),
            'ZIP not loaded')
