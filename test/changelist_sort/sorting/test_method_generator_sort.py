""" Testing The GeneratorSort Method.
"""
from changelist_data import ChangelistDataStorage

from changelist_sort import expand_changelists
from changelist_sort.sorting import generator_sort


def test_generator_sort_empty_input_empty_config_returns_empty_cl_map():
    test_input = []
    test_config = []
    result = generator_sort(test_input, test_config)
    assert len(result.get_lists()) == 0


def test_generator_sort_empty_input_empty_config_verbose_prints_zero_returns_empty():
    test_input = []
    test_config = []
    result = generator_sort(test_input, test_config)
    assert len(result.get_lists()) == 0


def test_generator_sort_simple_storage_input_empty_config_returns_cl_map(simple_storage: ChangelistDataStorage):
    test_input = expand_changelists(simple_storage.get_changelists())
    result = generator_sort(test_input, [])
    assert len(list(result.generate_nonempty_lists())) == 1


def test_generator_sort_multi_storage_input_empty_config_returns_cl_map(multi_storage: ChangelistDataStorage):
    test_input = expand_changelists(multi_storage.get_changelists())
    result = generator_sort(test_input, [])
    assert len(list(result.generate_nonempty_lists())) == 2