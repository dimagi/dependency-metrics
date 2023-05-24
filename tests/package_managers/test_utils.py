from unittest import TestCase, mock

from dependency_metrics.package_managers.utils import iter_outdated_packages


@mock.patch('dependency_metrics.package_managers.utils.get_outdated_packages')
class IterOutdatedPackagesTests(TestCase):

    def test_major_version_out_of_date(self, mock_outdated_packages):
        mock_outdated_packages.return_value = [
            {"name": "test", "version": "1.0", "latest_version": "5.0"}]
        result = list(iter_outdated_packages(mock.ANY))
        self.assertEqual(result, [([4, 0, 0], 'test', '5.0', '1.0')])

    def test_minor_version_out_of_date(self, mock_outdated_packages):
        mock_outdated_packages.return_value = [
            {"name": "test", "version": "1.0", "latest_version": "1.7"}]
        result = list(iter_outdated_packages(mock.ANY))
        self.assertEqual(result, [([0, 7, 0], 'test', '1.7', '1.0')])

    def test_patch_version_out_of_date(self, mock_outdated_packages):
        mock_outdated_packages.return_value = [
            {"name": "test", "version": "1.0.0", "latest_version": "1.0.10"}]
        result = list(iter_outdated_packages(mock.ANY))
        self.assertEqual(result, [([0, 0, 10], 'test', '1.0.10', '1.0.0')])

    def test_unknown_version(self, mock_outdated_packages):
        mock_outdated_packages.return_value = [
            {"name": "test", "version": "1.0.0", "latest_version": "unknown"}]
        result = list(iter_outdated_packages(mock.ANY))
        self.assertEqual(result, [(None, 'test', 'unknown', '1.0.0')])
