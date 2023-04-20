from package_metrics.constants import PIP
from package_metrics.package_managers.pip import get_pip_packages
from package_metrics.parsing_utils import behind


def iter_packages(package_manager):
    """
    Obtains packages given a manager, and builds package info tuple
    :param package_manager: str representing package manager
    :return: generator of package info (behind, name, latest, current)
    """
    for package_info in get_packages(package_manager):
        latest = package_info["latest_version"]
        current = package_info["version"]
        yield behind(latest, current), package_info["name"], latest, current


def get_packages(package_manager):
    """
    :param package_manager: str representing package manager
    :return: function to retrieve packages for the provided package manager
    """
    package_list_map = {
        PIP: get_pip_packages,
    }

    return package_list_map[package_manager]()
