from unittest import TestCase, mock

from dependency_metrics.package_managers.pip import (get_pip_packages,
                                                     get_total_count_for_pip)


@mock.patch('dependency_metrics.package_managers.pip.Pip')
class GetPipPackagesTests(TestCase):

    def test_returned_format_is_correct(self, mock_pip):
        # simulating what is returned by `pip list --format json --outdated`
        mock_pip.list.return_value = '[{"name": "test", "version": "1.0", ' \
                                     '"latest_version": "5.0", ' \
                                     '"latest_filetype": "wheel"}]'
        result = get_pip_packages()
        self.assertEqual(result, [
            {"name": "test", "version": "1.0", "latest_version": "5.0"}])


@mock.patch('dependency_metrics.package_managers.pip.Pip')
class GetTotalCountForPipTests(TestCase):

    def test_returns_accurate_count(self, mock_pip):
        mock_pip.list.return_value = '[{"name": "test", "version": "1.0", ' \
                                     '"latest_filetype": "wheel"}, {"name": ' \
                                     '"test2", "version": "5.1", ' \
                                     '"latest_filetype": "wheel"}]'
        result = get_total_count_for_pip()
        self.assertEqual(result, 2)
