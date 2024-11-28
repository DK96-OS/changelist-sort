"""The Input Package for Changelist Sort
"""
from pathlib import Path

from changelist_data.storage import load_storage
from changelist_data.storage.changelist_data_storage import ChangelistDataStorage
from changelist_data.storage.storage_type import StorageType

from changelist_sort.input.argument_data import ArgumentData
from changelist_sort.input.argument_parser import parse_arguments
from changelist_sort.input.input_data import InputData
from changelist_sort.sorting.sort_mode import SortMode


def validate_input(args_list: list[str]) -> InputData:
    """ Validate the arguments and gather program input into InputData object.
        - Parses command line strings into ArgumentData object.
        - Finds storage file and loads it into InputData as ChangelistDataStorage object.

    Returns:
    InputData - container for the program input.
    """
    arg_data = parse_arguments(args_list)
    return InputData(
        storage=_determine_storage_type(
            arg_data.changelists_path,
            arg_data.workspace_path,
        ),
        sort_mode=_determine_sort_mode(arg_data),
        remove_empty=arg_data.remove_empty,
    )


def _determine_storage_type(
    changelists_file: str | None,
    workspace_file: str | None,
) -> ChangelistDataStorage:
    # Check Path Args
    if changelists_file is not None:
        return load_storage(StorageType.CHANGELISTS, Path(changelists_file))
    if workspace_file is not None:
        return load_storage(StorageType.WORKSPACE, Path(workspace_file))
    # Search Default Paths
    return load_storage()


def _determine_sort_mode(arg_data: ArgumentData) -> SortMode:
    """ Check the Argument Data flags to determine which SortMode to use.
    """
    if arg_data.sourceset_sort:
        return SortMode.SOURCESET
    return SortMode.MODULE
