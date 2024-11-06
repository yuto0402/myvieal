def split_to_list(v: str, sep: str = ",") -> list[str]:
    return list(filter(None, map(str.strip, v.split(sep))))


def strtobool(v: str) -> bool:
    v = v.lower()
    if v in ("y", "yes", "t", "true", "on", "1"):
        return True
    if v in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"invalid truth value {v!r}")
