""" Manage Different Types of Modules
"""
from enum import Enum, auto


class ModuleType(Enum):
    MODULE = auto()
    ROOT = auto()
    GRADLE = auto()
    HIDDEN = auto()


def get_cl_simple_names(enum: ModuleType) -> tuple[str, ...]:
    """
    Obtain a tuple of simple names for changelists of a given ModuleType.
    """
    if enum == ModuleType.MODULE:
        return tuple()
    if enum == ModuleType.ROOT:
        return ('root', 'project', 'main')
    if enum == ModuleType.GRADLE:
        return ('buildupdates', 'gradle')
    if enum == ModuleType.HIDDEN:
        return tuple()
