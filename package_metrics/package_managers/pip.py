import json

from sh import Command


def get_pip_packages():
    """
    Return relevant package version info from pip list output
    """
    pip_packages = json.loads(Pip.list())
    cleaned_package_info_list = []
    for pkg_info in pip_packages:
        del pkg_info['latest_filetype']
        cleaned_package_info_list.append(pkg_info)
    return cleaned_package_info_list


class Pip:

    @staticmethod
    def list():
        """
        Equivalent to ``pip list --format json --outdated``
        """
        pip = Command("pip")
        return pip("list", "--format", "json", "--outdated")
