import json
import os
import time

import requests

from package_metrics.constants import (
    DATADOG_API_KEY,
    DATADOG_APP_KEY,
    GITHUB_ACTIONS,
    NOSE_DIVIDED_WE_RUN,
    MetricType,
)


def send_metric(name, value, metric_type, tags=None):
    """
    Send a specific metric to datadog
    :param name: name of metric
    :param value:
    :param metric_type: str in constants.MetricType
    :param tags: optional {key: value}, append additional tags to metric
           e.g., {"tag_name": "tag_value"}
    """

    api_key = os.environ[DATADOG_API_KEY]
    app_key = os.environ[DATADOG_APP_KEY]

    if metric_type not in MetricType.options():
        raise ValueError(
            f"Expected {metric_type} to be one of the following: "
            f"{MetricType.options()}")

    if os.environ.get(GITHUB_ACTIONS):
        host = 'github.com'
        ci_env = 'github_actions'
    else:
        host = 'unknown'
        ci_env = 'unknown'

    current_time = int(time.time())  # drop milliseconds from time.time()

    url = 'https://app.datadoghq.com/api/v1/series'
    headers = {
        'Content-type': 'application/json',
        'DD-API-KEY': api_key,
        'DD-APP-KEY': app_key,
    }

    tags = tags or {}
    tags['environment'] = ci_env
    if os.environ.get(NOSE_DIVIDED_WE_RUN):
        tags['partition'] = os.environ[NOSE_DIVIDED_WE_RUN]

    payload = {
        'series': [{
            'metric': name,
            'points': [[current_time, value]],
            'type': metric_type,
            'host': host,
            'tags': [f'{key}:{value}' for key, value in tags.items()]
        }]
    }
    requests.post(url, headers=headers, json=json.dumps(payload))
