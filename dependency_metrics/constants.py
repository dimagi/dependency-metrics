DATADOG_API_KEY = 'DATADOG_API_KEY'
DATADOG_APP_KEY = 'DATADOG_APP_KEY'
REPO = "REPO"

PIP = 'pip'
YARN = 'yarn'

UNKNOWN_VERSION = "unknown"


class MetricType:
    GAUGE = 'gauge'
    COUNT = 'count'
    RATE = 'rate'

    @classmethod
    def options(cls):
        return [cls.GAUGE, cls.COUNT, cls.RATE]
