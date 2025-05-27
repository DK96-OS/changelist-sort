""" Testing Changelist-Sort Method MapSort!
"""
from typing import Iterable

from changelist_sort import ChangelistData, sorting, expand_changelists, SortingChangelist
from changelist_sort.list_key import compute_key
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern
from test.input.conftest import simple_storage, multi_storage


def generate_changelists_1(
    changelists: list[ChangelistData],
) -> Iterable[ChangelistData]:
    """ Convert list into generator, which is Iterable.
    """
    for i in changelists:
        yield i


def test_simple_storage_changelists(simple_storage):
    test_input_generator = generate_changelists_1(expand_changelists(simple_storage.get_changelists()))
    result = list(test_input_generator)
    assert len(result) == 1
    assert 'Simple' == result[0].name


def test_multi_storage_changelists(multi_storage):
    test_input_generator = generate_changelists_1(expand_changelists(multi_storage.get_changelists()))
    result = list(test_input_generator)
    assert len(result) == 2
    assert 'Main' == result[0].name
    assert 'Test' == result[1].name


def test_map_sort_empty():
    test_input_generator = generate_changelists_1([])
    result = sorting.map_sort(test_input_generator, [])
    assert len(result.get_lists()) == 0


def test_map_sort_simple_storage_changelists_returns_old_and_new_changelists_sorted(simple_storage):
    test_input_generator = generate_changelists_1(expand_changelists(simple_storage.get_changelists()))
    result = sorting.map_sort(test_input_generator, [])
    result_lists = result.get_lists()
    # Quick non_empty_list check
    assert len(list(result.generate_nonempty_lists())) == 1
    # ChangelistMap Assertions
    # A new changelist has been created because of fallback to Module SortMode.
    assert len(result_lists) == 2
    assert result_lists[0].name == 'Simple'
    assert result_lists[1].name == 'Project Root'
    assert result_lists[0].id in result.changelist_ids
    assert result_lists[1].id in result.changelist_ids
    assert len(result.changelist_ids) == 2


def test_map_sort_multi_storage_empty_sort_config_returns_cl_map(multi_storage):
    test_input_generator = generate_changelists_1(expand_changelists(multi_storage.get_changelists()))
    result = sorting.map_sort(test_input_generator, [])
    # Quick non_empty_list check
    assert len(list(result.generate_nonempty_lists())) == 2
    # ChangelistMap Assertions
    # A new changelist has been created because of fallback to Module SortMode.
    assert len(result_lists := result.get_lists()) == 3
    assert result_lists[0].name == 'Main'
    assert result_lists[1].name == 'Test'
    assert result_lists[2].name == 'Project Root'
    assert result_lists[0].id in result.changelist_ids
    assert result_lists[1].id in result.changelist_ids
    assert result_lists[2].id in result.changelist_ids
    assert len(result.changelist_ids) == 3


def test_map_sort_multi_with_python_changelist_returns_cl_map(multi_storage):
    python_sorting_changelist = SortingChangelist(
        list_key=compute_key('Python Files'),
        file_patterns=[SortingFilePattern(file_ext='py')],
    )
    test_input_generator = generate_changelists_1(expand_changelists(multi_storage.get_changelists()))
    result = sorting.map_sort(test_input_generator, [python_sorting_changelist])
    # Quick non_empty_list check
    assert len(result_lists := list(result.generate_nonempty_lists())) == 1
    assert result_lists[0].name == 'Python Files'
    assert len(result_lists[0].changes) == 3
    # ChangelistMap Assertions
    # A new changelist has been created because of fallback to Module SortMode.
    assert len(result_lists := result.get_lists())
    assert result_lists[0].name == 'Main'
    assert result_lists[1].name == 'Test'
    assert result_lists[2].name == 'Python Files'
    assert result_lists[0].id in result.changelist_ids
    assert result_lists[1].id in result.changelist_ids
    assert result_lists[2].id in result.changelist_ids
    assert len(result.changelist_ids) == 3