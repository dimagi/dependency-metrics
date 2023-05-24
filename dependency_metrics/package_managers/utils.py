from dependency_metrics.constants import PIP, YARN
from dependency_metrics.package_managers.pip import (get_outdated_pip_packages,
                                                     get_total_count_for_pip)
from dependency_metrics.package_managers.yarn import (get_total_count_for_yarn,
                                                      get_outdated_yarn_packages)
from dependency_metrics.parsing_utils import behind


def iter_outdated_packages(package_manager):
    """
    Obtains packages given a manager, and builds package info tuple
    :param package_manager: str representing package manager
    :return: generator of package info (behind, name, latest, current)
    """
    for package_info in get_outdated_packages(package_manager):
        latest = package_info["latest_version"]
        current = package_info["version"]
        yield behind(latest, current), package_info["name"], latest, current


def get_outdated_packages(package_manager):
    """
    :param package_manager: str representing package manager
    :return: function to retrieve packages for the provided package manager
    """
    package_list_map = {
        PIP: get_outdated_pip_packages,
        YARN: get_outdated_yarn_packages,
    }

    return package_list_map[package_manager]()


def get_total_package_count(package_manager):
    """
    :param package_manager: str representing package manager
    :return: count of total number of packages installed via package manager
    """
    package_count_map = {
        PIP: get_total_count_for_pip,
        YARN: get_total_count_for_yarn,
    }

    return package_count_map[package_manager]()
