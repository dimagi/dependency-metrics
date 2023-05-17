import os
import time

import requests

from dependency_metrics.constants import (
    DATADOG_API_KEY,
    DATADOG_APP_KEY,
    PIP,
    REPO,
    YARN,
    MetricType,
)


def send_stats_to_datadog(stats, package_manager):
    """
    :param stats: key-value pairs representing outdated counts
    Example: {'major': 3, 'minor': 2, ...})
    :param package_manager: package manager used to collect statistics
    """
    metric_env = get_metric_name_for_package_manager(package_manager)
    metric_prefix = f"commcare.static_analysis.dependency.{metric_env}"
    for key, value in stats.items():
        metric_name = get_metric_name_for_stats_key(key)
        send_metric(f"{metric_prefix}.{metric_name}", value, MetricType.GAUGE)


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

    current_time = int(time.time())  # drop milliseconds from time.time()

    url = 'https://app.datadoghq.com/api/v1/series'
    headers = {
        'Content-type': 'application/json',
        'DD-API-KEY': api_key,
        'DD-APP-KEY': app_key,
    }

    tags = tags or {}
    payload = {
        'series': [{
            'metric': name,
            'points': [[current_time, value]],
            'type': metric_type,
            'host': os.environ.get(REPO) or 'unknown',
            'tags': [f'{key}:{value}' for key, value in tags.items()]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    if not response.ok:
        print(
            f"Post request to {url} failed with status code "
            f"{response.status_code} and error {response.text}\n"
            f"The payload sent was {payload}"
        )


def get_metric_name_for_package_manager(key):
    metric_name_map = {
        PIP: "python",
        YARN: "js",
    }
    return metric_name_map[key]


def get_metric_name_for_stats_key(key):
    metric_name_map = {
        "Outdated": "outdated",
        "Multi-Major": "multi_major_outdated",
        "Major": "major_outdated",
        "Minor": "minor_outdated",
        "Patch": "patch_outdated",
        "Unknown": "unknown"
    }
    return metric_name_map[key]

