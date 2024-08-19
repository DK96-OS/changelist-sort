""" Testing the Developer SortMode.
"""


from changelist_sort.sorting import sort
from changelist_sort.sorting.sort_mode import SortMode
from test import data_provider


def test_sort_dev_empty_returns_empty():
    test_input = []
    result = sort(test_input, SortMode.DEVELOPER)
    assert len(result) == 0


def test_sort_dev_build_updates_cl_sorted_returns_sorted():
    test_input = [data_provider.get_build_updates_changelist()]
    result = sort(test_input, SortMode.DEVELOPER)
    assert len(result) == 1
