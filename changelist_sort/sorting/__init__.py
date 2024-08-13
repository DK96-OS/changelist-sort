""" Sorting Package.
"""
from typing import Callable

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting.sort_mode import SortMode
from changelist_sort.sorting import module_sort
from changelist_sort.sorting.list_sort import split_changelist


def sort(
    initial_list: list[ChangelistData],
    sort_mode: SortMode,
) -> list[ChangelistData]:
    """
    Processes InputData.

    Parameters:
    - initial_list (list[ChangelistData]): The list of Changelists to be sorted.
    - sort_mode (SortMode): The SortMode determining which sort rules to apply.

    Returns:
    str - The desired output.
    """
    unsorted_files = []
    cl_map = ChangelistMap()
    for cl in initial_list:
        # Insert into Map
        cl_map.insert(cl)
        # Split The Changelist
        unsorted_files.extend(
            split_changelist(cl, _get_is_sorted_callable(sort_mode))
        )
    # This Callable depends on SortMode, which determines map keys
    sorting_callable = _create_sorting_callable(cl_map, sort_mode)
    for file in unsorted_files:
        sorting_callable(file)
    return cl_map.get_lists()


def _create_sorting_callable(
    changelist_map: ChangelistMap,
    sort_mode: SortMode,
) -> Callable[[ChangeData], bool]:
    """
    Create a Callable that sorts ChangeData passed to it.
    """
    if sort_mode == SortMode.MODULE:
        return lambda x: module_sort.sort_file_by_module(changelist_map, x)
    else:
        exit("SortMode not Implemented")


def _get_is_sorted_callable(
    sort_mode: SortMode
) -> Callable[[str, ChangeData], bool]:
    """
    Obtain a Callable that determines whether a ChangeData is sorted.
    """
    if sort_mode == SortMode.MODULE:
        return module_sort.is_sorted_by_module
    else:
        exit("SortMode not Implemented")
