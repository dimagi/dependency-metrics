import json

from sh import Command

from package_metrics.parsing_utils import behind


def iter_pip_packages():
    """
    Parse the output of ``pip list --format json --outdated``
    :return: generator containing version info for installed python packages
    """
    package_list = _get_pip_packages()
    for pkg in json.loads(package_list):
        latest = pkg["latest_version"]
        current = pkg["version"]
        yield behind(latest, current), pkg["name"], latest, current


def _get_pip_packages():
    """
    Equivalent to ``pip list --format json --outdated``
    """
    pip = Command("pip")
    return pip("list", "--format", "json", "--outdated")
