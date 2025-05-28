""" Sorting Package.
"""
from typing import Callable, Iterable, Generator

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import developer_sort, module_sort, source_set_sort
from changelist_sort.sorting.list_sort import split_changelist, generate_unsorted_change_data
from changelist_sort.sorting.sort_mode import SortMode
from changelist_sort.sorting.sorting_changelist import SortingChangelist


def sort(
    initial_list: Iterable[ChangelistData],
    sort_mode: SortMode,
    sorting_config: list[SortingChangelist] | None = None,
) -> list[ChangelistData]:
    """ Apply SortMode or Sorting Changelists to the Initial List.
 - sorting_config Changelists will override sort_mode, if not None.

**Parameters:**
 - initial_list (list[ChangelistData]): The list of Changelists to be sorted.
 - sort_mode (SortMode): The SortMode determining which sort rules to apply.
 - sorting_config (list[SortingChangelist]?): An optional list of SortingChangelist that contains rules for sorting.

**Returns:**
 list[ChangelistData] - The sorted Changelists.
    """
    if sorting_config is not None:
        return list(map_sort(initial_list, sorting_config).generate_lists())
    else:
        return list(_mode_sort(initial_list, sort_mode).generate_lists())


def map_sort(
    initial_list: Iterable[ChangelistData],
    sorting_config: list[SortingChangelist],
) -> ChangelistMap:
    """ Sort The Changelists using the SortingConfig and the ChangelistMap.

**Parameters:**
 - initial_list (Iterable[ChangelistData]): The Changelists before they are sorted.
 - sorting_config (list[SortingChangelist]): The changelist sorting criteria.

**Returns:**
 ChangelistMap - A data container class with the sorted changelists within.
    """
    _sort_it_out(
        (cl_map := ChangelistMap()),
        initial_list,
        is_sorted_callable=lambda key, cd: developer_sort.is_sorted_by_developer(key, cd, sorting_config),
        sorting_callable=lambda cd: developer_sort.sort_file_by_developer(cl_map, cd, sorting_config),
    )
    return cl_map


def generator_sort(
    initial_list: Iterable[ChangelistData],
    sorting_config: list[SortingChangelist],
) -> ChangelistMap:
    """ Sort The Changelists using the SortingConfig and the ChangelistMap.

**Parameters:**
 - initial_list (Iterable[ChangelistData]):
 - sorting_config (list[SortingChangelist]): The set of criteria describing the sort objective.
 - verbose (bool): Whether to print the total number of files sorted.

**Returns:**
 ChangelistMap -
    """
    for _ in _sort_it_out_generator(
        (cl_map := ChangelistMap()),
        initial_list,
        is_sorted_callable=lambda key, cd: developer_sort.is_sorted_by_developer(key, cd, sorting_config),
        sorting_callable=lambda cd: developer_sort.sort_file_by_developer(cl_map, cd, sorting_config),
    ):
        pass
    return cl_map


def _mode_sort(
    initial_list: Iterable[ChangelistData],
    sort_mode: SortMode,
) -> ChangelistMap:
    """ Sort Changelists using ChangelistMap and preset SortMode configurations.
    """
    cl_map = ChangelistMap()
    if sort_mode == SortMode.MODULE:
        _sort_it_out(
            cl_map,
            initial_list,
            module_sort.is_sorted_by_module,
            lambda cd: module_sort.sort_file_by_module(cl_map, cd)
        )
    elif sort_mode == SortMode.SOURCESET:
        _sort_it_out(
            cl_map,
            initial_list,
            source_set_sort.is_sorted_by_source_set,
            lambda cd: source_set_sort.sort_by_source_set(cl_map, cd)
        )
    else:
        exit("SortMode not Implemented")
    return cl_map


def _sort_it_out(
    cl_map: ChangelistMap,
    initial_list: Iterable[ChangelistData],
    is_sorted_callable: Callable[[ListKey, ChangeData], bool],
    sorting_callable: Callable[[ChangeData], bool]
):
    """
 - This method is called by higher level methods
    """
    unsorted = []
    for cl in initial_list:
        if not cl_map.insert(cl):
            _handle_map_insertion_error(cl_map, cl)
        # Extract Unsorted ChangeData using IsSortedCallable
        unsorted.extend(
            list_sort.generate_unsorted_change_data(cl, is_sorted_callable)
        )
    # Execute SortingCallable on each Unsorted File
    for cd in unsorted:
        sorting_callable(cd) # Ignore boolean result


def _sort_it_out_generator(
    cl_map: ChangelistMap,
    initial_list: Iterable[ChangelistData],
    is_sorted_callable: Callable[[ListKey, ChangeData], bool],
    sorting_callable: Callable[[ChangeData], bool]
) -> Generator[bool, None, None]:
    """
 - This method may be called by higher level methods.

**Yields:**
 bool - True, unless the sorting path of the ChangeData is None.
    """
    for cl in initial_list:
        if not cl_map.insert(cl):
            _handle_map_insertion_error(cl_map, cl)
    for cl in initial_list: # Extract Unsorted ChangeData using IsSortedCallable
        for cd in list_sort.generate_unsorted_change_data(cl, is_sorted_callable):
            yield sorting_callable(cd) # Execute SortingCallable on each Unsorted File


def _handle_map_insertion_error(
    cl_map: ChangelistMap,
    failure_cl: ChangelistData,
):
    """ Using the given parameters, produce an error message and exit.

    Raises:
    SystemExit - containing error information.
    """
    if (existing_cl := cl_map.search(failure_cl.list_key.key)) is not None:
        exit(f"Failed to Insert Changelist(name={failure_cl.name}) due to key conflict with Changelist(name={existing_cl.name}).")
    elif cl_map.contains_id(failure_cl.id):
        exit(f"Failed to Insert Changelist(name={failure_cl.name}) due to id conflict (id={failure_cl.id}).")
    else:
        exit(f"Failed to Insert Changelist(name={failure_cl.name}) for unknown reason (neither key nor id conflict has occurred).")