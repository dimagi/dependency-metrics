from unittest import TestCase

from dependency_metrics.parsing_utils import behind, parse_version


class BehindTests(TestCase):
    """
    Tests ``behind(latest, current)``
    """

    def test_major_delta(self):
        delta = behind("2.0.0", "1.0.0")
        self.assertEqual(delta, [1, 0, 0])

    def test_minor_delta(self):
        delta = behind("1.1.0", "1.0.0")
        self.assertEqual(delta, [0, 1, 0])

    def test_patch_delta(self):
        delta = behind("1.0.1", "1.0.0")
        self.assertEqual(delta, [0, 0, 1])

    def test_major_has_priority_over_minor(self):
        delta = behind("2.1.0", "1.0.0")
        self.assertEqual(delta, [1, 0, 0])

    def test_major_has_priority_over_patch(self):
        delta = behind("2.0.1", "1.0.0")
        self.assertEqual(delta, [1, 0, 0])

    def test_minor_has_priority_over_patch(self):
        delta = behind("1.1.1", "1.0.0")
        self.assertEqual(delta, [0, 1, 0])

    def test_multi_major_delta(self):
        delta = behind("5.0.0", "1.0.0")
        self.assertEqual(delta, [4, 0, 0])

    def test_multi_minor_delta(self):
        delta = behind("1.5.0", "1.0.0")
        self.assertEqual(delta, [0, 5, 0])

    def test_multi_patch_delta(self):
        delta = behind("1.0.5", "1.0.0")
        self.assertEqual(delta, [0, 0, 5])

    def test_unknown_latest_version(self):
        delta = behind("unknown", "1.0.0")
        self.assertEqual(delta, None)


class ParseVersionTests(TestCase):

    def test_major_minor_patch(self):
        version = parse_version("3.2.1")
        self.assertEqual(version, [3, 2, 1])

    def test_major_minor(self):
        version = parse_version("3.2")
        self.assertEqual(version, [3, 2, 0])

    def test_major(self):
        version = parse_version("3")
        self.assertEqual(version, [3, 0, 0])

    def test_non_semvar(self):
        version = parse_version("4.3.2.1")
        self.assertEqual(version, [4, 3, 2])

    def test_named_version(self):
        version = parse_version("alpha")
        self.assertEqual(version, [0, 0, 0])

    def test_combination_of_numbers_and_names(self):
        version = parse_version("2.1rc1")
        self.assertEqual(version, [2, 1, 0])

    def test_multi_digit_number_in_name(self):
        version = parse_version("2.10rc1")
        self.assertEqual(version, [2, 10, 0])

    def test_number_after_name_not_used(self):
        version = parse_version("3.a3.1")
        self.assertEqual(version, [3, 0, 1])
