import json
import os
from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time

from dependency_metrics.constants import MetricType
from dependency_metrics.datadog_utils import send_metric, send_stats_to_datadog


@patch('dependency_metrics.datadog_utils.send_metric')
def test_send_stats_to_datadog(mock_send_metric):
    stats = {'Outdated': 15}
    send_stats_to_datadog(stats, 'pip')
    mock_send_metric.assert_called_with(
        "commcare.static_analysis.dependency.python.outdated",
        15,
        MetricType.GAUGE)


@patch('dependency_metrics.datadog_utils.requests.post')
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
    def test_default_values(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.GAUGE)

        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload['series'][0]['metric'], 'name')
        self.assertEqual(payload['series'][0]['points'], [[1577874030, 'value']])
        self.assertEqual(payload['series'][0]['host'], 'unknown')

    def test_repository_set_as_host(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key',
                        REPO='test-repo')

        send_metric('name', 'value', MetricType.GAUGE)

        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload['series'][0]['host'], 'test-repo')

    def test_metric_type_is_gauge_when_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.GAUGE)

        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload['series'][0]['type'], MetricType.GAUGE)

    def test_metric_type_is_count_when_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.COUNT)

        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload['series'][0]['type'], MetricType.COUNT)

    def test_metric_type_is_rate_when_set(self, mock_post):
        self._setup_env(DATADOG_API_KEY='api_key', DATADOG_APP_KEY='app_key')

        send_metric('name', 'value', MetricType.RATE)

        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        self.assertEqual(payload['series'][0]['type'], MetricType.RATE)

    def _setup_env(self, **kwargs):
        """
        Useful to simplify test setup
        """
        for key, value in kwargs.items():
            os.environ[key] = value
            self.addCleanup(os.environ.pop, key)
