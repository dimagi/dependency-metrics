import json
import os
from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time

from package_metrics.constants import MetricType
from package_metrics.datadog_utils import send_metric


@patch('package_metrics.datadog_utils.requests.post')
class SendMetricTests(TestCase):

    def test_raises_error_if_api_key_not_found(self, mock_post):
        self._setup_env(DATADOG_APP_KEY='app_key')

        with self.assertRaises(KeyError):
            send_metric('name', 'value', MetricType.GAUGE)

    def test_raises_error_if_app_key_not_found(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key')

        with self.assertRaises(KeyError):
            send_metric('name', 'value', MetricType.GAUGE)

    def test_raises_error_if_metric_type_not_valid(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        with self.assertRaises(ValueError):
            send_metric('name', 'value', 'invalid')

    @freeze_time('2020-01-01 10:20:30')
    def test_default_json_payload_values_are_correct(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.GAUGE)

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['series'][0]['metric'], 'name')
        self.assertEqual(payload['series'][0]['points'], [[1577874030, 'value']])
        self.assertEqual(payload['series'][0]['host'], 'unknown')
        self.assertEqual(payload['series'][0]['tags'][0]['environment'],
                         'unknown')

    def test_host_and_environment_is_github_when_in_github_action(self, mock_post):
        """
        The GITHUB_ACTIONS environment variable is set when running from a
        github action
        """
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key',
                        GITHUB_ACTIONS='test')

        send_metric('name', 'value', MetricType.GAUGE)

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['series'][0]['host'], 'github.com')
        self.assertEqual(payload['series'][0]['tags'][0]['environment'],
                         'github_actions')

    def test_metric_type_is_gauge_when_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.GAUGE)

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['series'][0]['type'], MetricType.GAUGE)

    def test_metric_type_is_count_when_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.COUNT)

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['series'][0]['type'], MetricType.COUNT)

    def test_metric_type_is_rate_when_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.RATE)

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['series'][0]['type'], MetricType.RATE)

    def test_partition_is_correct_when_nose_divided_we_run_is_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key',
                        NOSE_DIVIDED_WE_RUN='1')

        send_metric('name', 'value', MetricType.RATE)

        args, kwargs = mock_post.call_args
        payload = json.loads(kwargs['json'])
        self.assertEqual(payload['series'][0]['tags'][0]['partition'], '1')

    def _setup_env(self, **kwargs):
        """
        Useful to simplify test setup
        """
        for key, value in kwargs.items():
            os.environ[key] = value
            self.addCleanup(os.environ.pop, key)