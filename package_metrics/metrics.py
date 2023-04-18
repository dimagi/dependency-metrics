import argparse

from package_metrics.package_managers.pip import parse_pip


def get_packages(package_manager):
    parsers = {
        "pip": parse_pip,
    }
    return parsers[package_manager]()


def build_packages_table(packages):
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


def main():
    parser = argparse.ArgumentParser(
        description="Track dependencies of a project"
    )
    parser.add_argument(
        "package_manager",
        help="package manager to calculate metrics for",
        choices=["pip"]
    )
    args = parser.parse_args()

    packages = get_packages(args.package_manager)
    package_table = build_packages_table(packages)
    for row in package_table:
        print(row)


if __name__ == "__main__":
    main()
