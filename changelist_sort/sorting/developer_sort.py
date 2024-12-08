""" Sort With Developer File Patterns.
"""
from typing import Iterable, Callable

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import file_sort, module_sort
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_changelist import SortingChangelist


def filter_patterns_by_module(
    module_type: ModuleType | None,
    cl_patterns: Iterable[SortingChangelist],
) -> list[SortingChangelist]:
    """ Filter the Changelists by the ModuleType their Pattern applies to.
    """
    return list(filter(
        lambda dcl: dcl.module_type is None or dcl.module_type == module_type,
        cl_patterns
    ))


def sort_file_by_developer(
    cl_map: ChangelistMap,
    file: ChangeData,
    sorting_config=None,
) -> bool:
    """ Apply the Developer FilePattern Setting to Sort a single File into the Changelist Map.
        - Filters Patterns by matching ModuleType before checking files.
        - Fallback to Module Sort
    """
    # Filter Developer Changelist Tuple by File's ModuleType 
    if sorting_config is None:
        return module_sort.sort_file_by_module(cl_map, file)
    filtered_dcl_patterns = filter_patterns_by_module(
        file_sort.get_module_type(file),
        sorting_config,
    )
    # Check Developer Changelists in Tuple Order
    for dcl_pattern in filtered_dcl_patterns:
        if dcl_pattern.check_file(file):
            # Pattern Matched.
            # Search Map. Add File to Changelist.
            if (cl := cl_map.search(dcl_pattern.list_key.key)) is not None:
                cl.changes.append(file)
                return True
            # Create the Developer Changelist. Add File to Changelist.
            cl_map.create_changelist(dcl_pattern.list_key.changelist_name).changes.append(file)
            return True
    # Fallback to Module Sort when Developer Sort Fails.
    return module_sort.sort_file_by_module(cl_map, file)


def create_is_sorted_by_developer(sorting_config) -> Callable[[ListKey, ChangeData], bool]:
    return lambda x, y: is_sorted_by_developer(x, y, sorting_config)


def is_sorted_by_developer(
    changelist_key: ListKey,
    file: ChangeData,
    sorting_config: list[SortingChangelist],
) -> bool:
    """ Determines if this File matches the ChangeList Key or Name.
        - Finds the First DeveloperChangelist Pattern that matches
        - Fallback to Module Sort
    """
    # Filter Developer Changelist Tuple by File's ModuleType 
    filtered_dcl_patterns = filter_patterns_by_module(
        file_sort.get_module_type(file),
        sorting_config,
    )
    # Check Developer Changelists in Tuple Order
    for dcl_pattern in filtered_dcl_patterns:
        if dcl_pattern.check_file(file):
            # Pattern Matched
            if dcl_pattern.list_key.key == changelist_key.key or\
                dcl_pattern.list_key.changelist_name == changelist_key.changelist_name:
                return True
            # This File could be sorted higher in the Developer Changelist order.
            return False
    # Fallback to Module Sort.
    return module_sort.is_sorted_by_module(changelist_key, file)
