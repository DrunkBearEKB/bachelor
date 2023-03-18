from typing import Type


def resolve(name: str) -> Type:
    """
    Resolve import path to actual object.
    """
    parts = name.split(".")

    used = parts.pop(0)
    found = __import__(used)
    for part in parts:
        used += "." + part
        try:
            found = getattr(found, part)
        except AttributeError:
            pass
        else:
            continue
        try:
            __import__(used)
        except ImportError as exc:
            expected = str(exc).split()[-1]
            if expected == used:
                raise
            else:
                raise ImportError(f"import error in {used}: {exc}")
        found = getattr(found, part)
    return found
