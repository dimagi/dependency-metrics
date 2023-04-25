DATADOG_API_KEY = 'DATADOG_API_KEY'
DATADOG_APP_KEY = 'DATADOG_APP_KEY'

GITHUB_ACTIONS = 'GITHUB_ACTIONS'

NOSE_DIVIDED_WE_RUN = 'NOSE_DIVIDED_WE_RUN'

PIP = 'pip'
YARN = 'yarn'


class MetricType:
    GAUGE = 'gauge'
    COUNT = 'count'
    RATE = 'rate'

    @classmethod
    def options(cls):
        return [cls.GAUGE, cls.COUNT, cls.RATE]
