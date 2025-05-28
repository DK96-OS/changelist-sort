""" Testing the Hidden Package Method handle_map_insertion_error
"""
import pytest

from changelist_sort.changelist_data import expand
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting import _handle_map_insertion_error


def test_handle_map_insertion_error_raises_exit_message(simple_storage):
    cl_map = ChangelistMap()
    failed_cl = expand(simple_storage.get_changelists()[0])
    with pytest.raises(SystemExit, match='Failed to Insert Changelist'):
        _handle_map_insertion_error(cl_map, failed_cl)