from sh import Command

from package_metrics.exceptions import Crash


def get_yarn_packages():
    version = Yarn.version()
    if not version.startswith("1."):
        raise Crash(f"Yarn Classic (v1.x) is required, found {version}")

    outdated_packages = []
    for package in parse_yarn_list():
        latest_version = pull_latest_version(package["name"])
        if package["version"] != latest_version:
            # only care if it is actually outdated
            # TODO: handle when latest_version is None
            package["latest_version"] = latest_version
            outdated_packages.append(package)
    return outdated_packages


def pull_latest_version(package_name):
    lines = Yarn.latest_version(package_name)
    if not lines:
        return None
    # trim first and last line from output as they are irrelevant
    lines = lines.splitlines()[1:-1]
    assert len(lines) == 1, f"{package_name}: invalid latest: {lines!r}"
    return lines[0].strip()


def parse_yarn_list():
    """
    Parse output of ``Yarn.list`` into list of package name and version dicts
    """
    packages = []
    yarn_list = Yarn.list()
    # trim first and last line from output as they are irrelevant
    for line in yarn_list.splitlines()[1:-1]:
        line = line.rstrip()
        if not line:
            continue
        # example:
        # ├─ @ungap/promise-all-settled@1.1.2
        # ├─ abbrev@1.1.1
        name, x, version = line.split(None, 2)[1].rpartition("@")
        packages.append({"name": name, "version": version})
    return packages


class Yarn:
    """
    Class to house raw yarn commands
    NOTE: avoid using --json option because the output includes a lot of
    irrelevant lines
    """

    @staticmethod
    def latest_version(package_name):
        """
        Equivalent to ``yarn info <package_name> dist-tags.latest``
        """
        yarn = Command("yarn")
        return yarn("info", package_name, "dist-tags.latest")

    @staticmethod
    def list():
        """
        Equivalent to ``yarn list --depth 0``
        """
        yarn = Command("yarn")
        return yarn("list", "--depth", "0")

    @staticmethod
    def version():
        """
        Equivalent to ``yarn --version``
        """
        yarn = Command("yarn")
        return yarn("--version")
