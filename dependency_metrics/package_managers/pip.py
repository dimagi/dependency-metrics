import json
import os
import sys
from pathlib import Path

import sh


def get_outdated_pip_packages():
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
        venv = os.environ.get("VIRTUAL_ENV")
        if not venv:
            print("WARNING: VIRTUAL_ENV is not set.", file=sys.stderr)
        else:
            venv = Path(venv)

        args = ["list", "--format", "json"]
        if outdated:
            args.append("--outdated")

        try:
            return sh.uv("pip", *args)
        except sh.CommandNotFound:
            pass  # fall back to pip

        if not venv:
            pip = sh.pip
        elif (venv / "bin/pip").exists():
            pip = sh.Command(venv / "bin/pip")
        else:
            # pip may exist outside the active virtualenv, and may list
            # packages from somewhere else on the system.
            print("WARNING: pip not found in virtualenv. "
                  f"Using --python={venv}", file=sys.stderr)
            pip = sh.pip.bake(python=venv)
        return pip(*args)
