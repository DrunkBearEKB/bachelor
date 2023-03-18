from typing import Set, Type, Any


def get_all_subclasses(cls: Type[Any]) -> Set[Type[Any]]:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )
