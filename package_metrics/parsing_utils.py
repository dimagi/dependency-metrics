def behind(latest, current):
    delta = [0, 0, 0]
    for index, (lat, cur) in enumerate(zip(vsplit(latest), vsplit(current))):
        if lat != cur:
            delta[index] = lat - cur
            break
    return delta


def vsplit(version):
    padded = f"{version}.0.0"  # append extra zeros for versions like '1' or '2.0'
    return [int(n) for n in padded.split(".")[:3]]

