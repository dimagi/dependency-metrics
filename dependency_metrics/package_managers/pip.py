import json

import sh


def get_pip_packages():
    """
    Return relevant package version info from pip list output
    """
    pip_packages = json.loads(Pip.list(outdated=True))
    cleaned_package_info_list = []
    for pkg_info in pip_packages:
        del pkg_info['latest_filetype']
        cleaned_package_info_list.append(pkg_info)
    return cleaned_package_info_list


def get_total_count_for_pip():
    """
    Return total number of installed dependencies
    """
    packages = json.loads(Pip.list())
    return len(packages)


class Pip:

    @staticmethod
    def list(outdated=False):
        """
        Equivalent to ``pip list --format json [--outdated]``
        """
        args = ["list", "--format", "json"]
        if outdated:
            args.append("--outdated")
        return sh.pip(*args)
