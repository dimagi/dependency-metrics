from unittest import TestCase

from package_metrics.parsing_utils import behind, vsplit


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


class VsplitTests(TestCase):

    def test_major_minor_patch(self):
        version = vsplit("3.2.1")
        self.assertEqual(version, [3, 2, 1])

    def test_major_minor(self):
        version = vsplit("3.2")
        self.assertEqual(version, [3, 2, 0])

    def test_major(self):
        version = vsplit("3")
        self.assertEqual(version, [3, 0, 0])

    def test_non_semvar(self):
        version = vsplit("4.3.2.1")
        self.assertEqual(version, [4, 3, 2])
