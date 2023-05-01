import argparse

from dependency_metrics.constants import PIP, YARN
from dependency_metrics.datadog_utils import send_stats_to_datadog
from dependency_metrics.package_managers.utils import iter_packages


def build_packages_table(packages):
    """ Builds a table representing how out of date dependencies are
    Example:
    Behind   Package                      Latest       Version
    n/a      At.js                        exotic       1.5.3
    ...
    0.0.1    bootstrap-timepicker         0.5.2        0.5.1
    ...
    12.0.0   sinon                        14.0.0       2.3.2
    """
    def build_row(behind, name, current, latest):
        return f"{behind:8s} {name:28s} {current:12s} {latest}"

    rows = [build_row("Behind", "Package", "Latest", "Version")]

    records = sorted(packages)
    for delta, name, current, latest in records:
        if delta:
            behind = ".".join(str(v) for v in delta)
        else:
            behind = "n/a"
        rows.append(build_row(behind, name, current, latest))

    return rows


def get_package_stats(packages):
    """Displays a count for each version category of out of date dependencies"""
    stats = {
        "Outdated": 0,
        "Multi-Major": 0,
        "Major": 0,
        "Minor": 0,
        "Patch": 0,
        "Unknown": 0,
    }
    for delta, name, current, latest in packages:
        if delta:
            major, minor, patch = delta
            if major:
                assert not minor and not patch, delta
                if major == 1:
                    key = "Major"
                else:
                    key = "Multi-Major"
            elif minor:
                assert not major and not patch, delta
                key = "Minor"
            else:
                assert patch and not major and not minor, delta
                key = "Patch"
        else:
            key = "Unknown"
        stats[key] += 1
        stats["Outdated"] += 1
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Track dependencies of a project"
    )
    parser.add_argument(
        "package_manager",
        help="package manager to calculate metrics for",
        choices=[PIP, YARN]
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--stats",
        help="generate statistics and output to stdout",
        default=False,
        action="store_true",
    )
    group.add_argument(
        "--send",
        help="generate statistics and send to datadog",
        default=False,
        action="store_true"
    )
    args = parser.parse_args()

    packages = iter_packages(args.package_manager)
    if args.stats or args.send:
        stats = get_package_stats(packages)
        if args.stats:
            # NOTE: subtle detail: we're depending on Python 3's ordered dict to
            # maintain deterministic ordering here
            for key, value in stats.items():
                print(f"{key}: {value}")
        elif args.send:
            send_stats_to_datadog(stats, args.package_manager)

    else:
        package_table = build_packages_table(packages)
        for row in package_table:
            print(row)


if __name__ == "__main__":
    main()
