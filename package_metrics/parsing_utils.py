import re


def behind(latest, current):
    if latest == 'unknown':
        return None
    delta = [0, 0, 0]
    parsed_latest = parse_version(latest)
    parsed_current = parse_version(current)
    for index, (lat, cur) in enumerate(zip(parsed_latest, parsed_current)):
        if lat != cur:
            delta[index] = lat - cur
            break
    return delta


def parse_version(version):
    """
    :param version: a string representing the package version (e.g., '1.0.1')
    :return: a list of integers representing [major, minor, patch]
    """
    padded = f"{version}.0.0"  # append extra zeros for versions like '1' or '2.0'
    semvar_version = []
    for n in padded.split(".")[:3]:
        try:
            num = int(n)
        except ValueError:
            match = re.search(r'^\d+', n)
            # default to 0, unless
            num = int(match.group()) if match else 0
        semvar_version.append(num)

    return semvar_version

