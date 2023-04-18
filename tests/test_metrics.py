from unittest import TestCase

from package_metrics.metrics import build_packages_table


class BuildPackagesTableTests(TestCase):

    def test_header_row(self):
        packages = []
        rows = build_packages_table(packages)
        self.assertEqual(rows[0], "Behind   Package                      Latest       Version")

    def test_row_with_delta(self):
        packages = [([0, 1, 0], 'test', '1.1', '1.0')]
        rows = build_packages_table(packages)
        self.assertEqual(rows[1], "0.1.0    test                         1.1          1.0")

    def test_row_with_no_delta(self):
        packages = [([0, 0, 0], 'test', '1.0', '1.0')]
        rows = build_packages_table(packages)
        self.assertEqual(rows[1], "0.0.0    test                         1.0          1.0")
