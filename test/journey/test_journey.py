import unittest

import journey


class VersionTestCase(unittest.TestCase):
    def test_version_present(self):
        self.assertTrue(
            hasattr(journey, 'VERSION'), 'No version present')
