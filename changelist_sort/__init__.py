""" Main Package Methods.
"""
from typing import Iterable, Generator

from changelist_data import ChangelistDataStorage
from changelist_data.changelist import Changelist

from changelist_sort.changelist_data import ChangelistData, generate_simple_changelists, generate_expanded_changelists
from changelist_sort.input.input_data import InputData
from changelist_sort.sorting import sort, SortMode, SortingChangelist, map_sort


def sort_changelists(
    input_data: InputData,
):
    """ Sort the given Changelists and write them to the Workspace File.
    """
    sort_changelist_in_storage(
        input_data.storage,
        input_data.sort_mode,
        input_data.remove_empty,
        input_data.sorting_config,
    )
    #Todo: Remove this write_to_storage in Version 0.5, not within scope
    # The storage call is to be made by main method.
    input_data.storage.write_to_storage()


def sort_changelist_in_storage(
    storage: ChangelistDataStorage,
    sort_mode: SortMode,
    remove_empty: bool,
    sorting_config: list[SortingChangelist],
):
    """ Sort the Changelists in Storage, and update them.
    """
    changelists = sort(
        initial_list=generate_expanded_changelists(storage.generate_changelists()),
        sort_mode=sort_mode,
        sorting_config=sorting_config,
    )
    storage.update_changelists(
        generate_simple_changelists(changelists) if not remove_empty else filter(
            lambda x: len(x.changes) > 0, generate_simple_changelists(changelists)
        )
    )


def sort_and_filter(
    data: Iterable[ChangelistData],
    sorting_config: list[SortingChangelist],
    sort_mode: SortMode = SortMode.MODULE,
    filter_empty: bool = True,
) -> Generator[ChangelistData, None, None]:
    """
**Parameters:**
 - data (Iterable[ChangelistData]): The input data.
 - sort_mode (SortMode): The mode to apply in absence of sorting_config.
 - sorting_config (list[SortingChangelist]): The Sorting Changelists configuration.
 - apply_filter (bool): Filter out Empty Changelists. Default: True.

**Yields:**
 ChangelistData - The sorted ChangelistData objects.
    """
    cl_map = map_sort(data, sorting_config)
    #
    if filter_empty:
        yield from cl_map.generate_nonempty_lists()
    else:
        yield from cl_map.generate_lists()


def simplify_changelists(
    data: Iterable[ChangelistData]
) -> list[Changelist]:
    return list(generate_simple_changelists(data))


def expand_changelists(
    data: Iterable[Changelist]
) -> list[ChangelistData]:
    return list(generate_expanded_changelists(data))