from unittest import TestCase, mock

from package_metrics.package_managers.pip import parse_pip


@mock.patch('package_metrics.package_managers.pip._get_pip_packages')
class ParsePipTests(TestCase):

    def test_major_version_out_of_date(self, mock_packages):
        mock_packages.return_value = '[{"name": "test", "version": "1.0", ' \
                                     '"latest_version": "5.0", ' \
                                     '"latest_filetype": "wheel"}]'
        result = list(parse_pip())
        self.assertEqual(result, [([4, 0, 0], 'test', '5.0', '1.0')])

    def test_minor_version_out_of_date(self, mock_packages):
        mock_packages.return_value = '[{"name": "test", "version": "1.0", ' \
                                     '"latest_version": "1.7", ' \
                                     '"latest_filetype": "wheel"}]'
        result = list(parse_pip())
        self.assertEqual(result, [([0, 7, 0], 'test', '1.7', '1.0')])

    def test_patch_version_out_of_date(self, mock_packages):
        mock_packages.return_value = '[{"name": "test", "version": "1.0.0", ' \
                                     '"latest_version": "1.0.10", ' \
                                     '"latest_filetype": "wheel"}]'
        result = list(parse_pip())
        self.assertEqual(result, [([0, 0, 10], 'test', '1.0.10', '1.0.0')])

    def test_major_has_priority_over_minor(self, mock_packages):
        mock_packages.return_value = '[{"name": "test", "version": "1.0.0", ' \
                                     '"latest_version": "2.4.0", ' \
                                     '"latest_filetype": "wheel"}]'
        result = list(parse_pip())
        self.assertEqual(result, [([1, 0, 0], 'test', '2.4.0', '1.0.0')])

    def test_major_has_priority_over_patch(self, mock_packages):
        mock_packages.return_value = '[{"name": "test", "version": "1.0.0", ' \
                                     '"latest_version": "2.0.1", ' \
                                     '"latest_filetype": "wheel"}]'
        result = list(parse_pip())
        self.assertEqual(result, [([1, 0, 0], 'test', '2.0.1', '1.0.0')])

    def test_minor_has_priority_over_patch(self, mock_packages):
        mock_packages.return_value = '[{"name": "test", "version": "1.0.0", ' \
                                     '"latest_version": "1.5.1", ' \
                                     '"latest_filetype": "wheel"}]'
        result = list(parse_pip())
        self.assertEqual(result, [([0, 5, 0], 'test', '1.5.1', '1.0.0')])
