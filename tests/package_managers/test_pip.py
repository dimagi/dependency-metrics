from unittest import TestCase, mock

from package_metrics.package_managers.pip import get_pip_packages


@mock.patch('package_metrics.package_managers.pip.Pip')
class GetPipPackagesTests(TestCase):

    def test_returned_format_is_correct(self, mock_pip):
        # simulating what is returned by `pip list --format json --outdated`
        mock_pip.list.return_value = '[{"name": "test", "version": "1.0", ' \
                                     '"latest_version": "5.0", ' \
                                     '"latest_filetype": "wheel"}]'
        result = get_pip_packages()
        self.assertEqual(result, [
            {"name": "test", "version": "1.0", "latest_version": "5.0"}])
