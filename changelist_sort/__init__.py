""" Main Package Methods.
"""
from typing import Iterable, Generator

from changelist_data import ChangelistDataStorage
from changelist_data.changelist import Changelist

from changelist_sort.changelist_data import ChangelistData, generate_simple_changelists, \
    generate_expanded_changelists
from changelist_sort.input import input_data
from changelist_sort.input.input_data import InputData
from changelist_sort.sorting import sort, SortMode, SortingChangelist


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
    storage.update_changelists(
        simplify_changelists(
            _sort_and_filter(
                data=generate_expanded_changelists(
                    storage.generate_changelists()
                ),
                sort_mode=sort_mode,
                sorting_config=sorting_config,
                apply_filter=remove_empty,
            )
        )
    )


def _sort_and_filter(
    data: Iterable[ChangelistData],
    sort_mode: SortMode,
    sorting_config,
    apply_filter: bool = True,
) -> Generator[ChangelistData, None, None]:
    """
**Parameters:**
 - data: ():
 -
 - apply_filter (bool): Filter out Empty Changelists. Default: True.
    """
    cl_map = sorting.map_sort(data, sorting_config)
    if apply_filter:
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