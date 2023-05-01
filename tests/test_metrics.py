from unittest import TestCase

from dependency_metrics.metrics import build_packages_table, get_package_stats


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


class GetPackageStatsTests(TestCase):

    def test_outdated_multi_major_package(self):
        packages = [([2, 0, 0], 'test', '3.1', '1.0')]
        stats = get_package_stats(packages)
        self.assertEqual(stats, {
            "Outdated": 1,
            "Multi-Major": 1,
            "Major": 0,
            "Minor": 0,
            "Patch": 0,
            "Unknown": 0,
        })

    def test_outdated_major_package(self):
        packages = [([1, 0, 0], 'test', '2.5', '1.0')]
        stats = get_package_stats(packages)
        self.assertEqual(stats, {
            "Outdated": 1,
            "Multi-Major": 0,
            "Major": 1,
            "Minor": 0,
            "Patch": 0,
            "Unknown": 0,
        })

    def test_outdated_minor_package(self):
        packages = [([0, 5, 0], 'test', '2.5', '2.0')]
        stats = get_package_stats(packages)
        self.assertEqual(stats, {
            "Outdated": 1,
            "Multi-Major": 0,
            "Major": 0,
            "Minor": 1,
            "Patch": 0,
            "Unknown": 0,
        })

    def test_outdated_patch_package(self):
        packages = [([0, 0, 3], 'test', '2.5.4', '2.5.1')]
        stats = get_package_stats(packages)
        self.assertEqual(stats, {
            "Outdated": 1,
            "Multi-Major": 0,
            "Major": 0,
            "Minor": 0,
            "Patch": 1,
            "Unknown": 0,
        })

    def test_unknown_package(self):
        packages = [(None, 'test', 'unknown', '2.5.1')]
        stats = get_package_stats(packages)
        self.assertEqual(stats, {
            "Outdated": 1,
            "Multi-Major": 0,
            "Major": 0,
            "Minor": 0,
            "Patch": 0,
            "Unknown": 1,
        })
