from textwrap import dedent
from unittest import TestCase, mock
from unittest.mock import patch

from dependency_metrics.exceptions import Crash
from dependency_metrics.package_managers.yarn import (
    get_yarn_packages,
    parse_yarn_list,
    pull_latest_version
)


class GetYarnPackagesTests(TestCase):

    @patch('dependency_metrics.package_managers.yarn.Yarn')
    def test_exception_raised_if_wrong_yarn_version(self, mock_yarn):
        mock_yarn.version.return_value = "2.0"
        with self.assertRaises(Crash):
            get_yarn_packages()

    @patch('dependency_metrics.package_managers.yarn.parse_yarn_list')
    @patch('dependency_metrics.package_managers.yarn.pull_latest_version')
    def test_correct_format_is_returned(self, mock_latest_version, mock_yarn_list):
        mock_latest_version.return_value = "5.0.0"
        mock_yarn_list.return_value = [{"name": "test", "version": "1.0.0"}]

        packages = get_yarn_packages()

        self.assertEqual(packages, [
            {"name": "test", "version": "1.0.0", "latest_version": "5.0.0"}])

    @patch('dependency_metrics.package_managers.yarn.parse_yarn_list')
    @patch('dependency_metrics.package_managers.yarn.pull_latest_version')
    def test_unknown_latest_version(self, mock_latest_version, mock_yarn_list):
        mock_latest_version.return_value = None
        mock_yarn_list.return_value = [{"name": "test", "version": "1.0.0"}]

        packages = get_yarn_packages()

        self.assertEqual(packages, [
            {"name": "test", "version": "1.0.0", "latest_version": "unknown"}])


@patch('dependency_metrics.package_managers.yarn.Yarn.list')
class ParseYarnListTests(TestCase):

    def test_expected_output_is_parsed_successfully(self, mock_yarn_list):
        mock_yarn_list.return_value = dedent("""yarn list v1.22.19
        ├─ @test/package@3.2.1
        ├─ test@5.0
        Done in 0.0s.""")
        packages = parse_yarn_list()
        self.assertEqual(packages,
                         [{"name": "@test/package", "version": "3.2.1"},
                          {"name": "test", "version": "5.0"}])

    def test_blank_line_is_skipped(self, mock_yarn_list):
        mock_yarn_list.return_value = dedent("""yarn list v1.22.19
        
        Done in 0.0s.""")
        packages = parse_yarn_list()
        self.assertEqual(packages, [])

    def test_whitespace_is_handled(self, mock_yarn_list):
        mock_yarn_list.return_value = dedent("""yarn list v1.22.19
        ├─             test@5.0
        Done in 0.0s.""")
        packages = parse_yarn_list()
        self.assertEqual(packages, [{"name": "test", "version": "5.0"}])


@patch('dependency_metrics.package_managers.yarn.Yarn.latest_version')
class PullLatestVersionTests(TestCase):

    def test_returns_latest_version_successfully(self, mock_latest_version):
        mock_latest_version.return_value = dedent("""yarn info v1.22.19
        5.0.0
        Done in 0.16s.""")
        latest_version = pull_latest_version(mock.ANY)
        self.assertEqual(latest_version, "5.0.0")

    def test_returns_none_if_latest_version_is_empty(self, mock_latest_version):
        mock_latest_version.return_value = None
        latest_version = pull_latest_version(mock.ANY)
        self.assertIsNone(latest_version)

    def test_raises_assertion_error_if_output_line_count_mismatch(self, mock_latest_version):
        mock_latest_version.return_value = "5.0.0"
        with self.assertRaises(AssertionError):
            pull_latest_version(mock.ANY)
