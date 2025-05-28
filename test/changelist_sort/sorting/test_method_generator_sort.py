""" Testing The GeneratorSort Method.
"""
from changelist_data import ChangelistDataStorage

from changelist_sort import expand_changelists
from changelist_sort.sorting import generator_sort


def test_generator_sort_empty_input_empty_config_returns_empty_cl_map():
    test_input = []
    test_config = []
    result = list(generator_sort(test_input, test_config))
    assert len(result) == 0


def test_generator_sort_empty_input_empty_config_verbose_prints_zero_returns_empty():
    test_input = []
    test_config = []
    result = list(generator_sort(test_input, test_config))
    assert len(result) == 0


def test_generator_sort_simple_storage_input_empty_config_returns_cl_map(simple_storage: ChangelistDataStorage):
    test_input = expand_changelists(simple_storage.get_changelists())
    result = list(generator_sort(test_input, [], True))
    assert len(list(result)) == 1


def test_generator_sort_simple_storage_input_empty_config_no_filter_returns_2(simple_storage: ChangelistDataStorage):
    test_input = expand_changelists(simple_storage.get_changelists())
    result = list(generator_sort(test_input, [], False))
    assert len(list(result)) == 2


def test_generator_sort_multi_storage_input_empty_config_filter_returns_2(multi_storage: ChangelistDataStorage):
    test_input = expand_changelists(multi_storage.get_changelists())
    result = list(generator_sort(test_input, [], True))
    assert len(list(result)) == 2


def test_generator_sort_multi_storage_input_empty_config_no_filter_returns_3(multi_storage: ChangelistDataStorage):
    test_input = expand_changelists(multi_storage.get_changelists())
    result = list(generator_sort(test_input, [], False))
    assert len(result) == 3
    assert result[0].name == 'Main'
    assert result[1].name == 'Test'
    assert result[2].name == 'Project Root'


def test_generator_sort_multi_storage_dev_cl0_config_filter_returns_2(
    multi_storage: ChangelistDataStorage,
    sort_config_developer_cl_0
):
    test_input = expand_changelists(multi_storage.get_changelists())
    result = list(generator_sort(test_input, sort_config_developer_cl_0, True))
    assert len(result) == 2
    assert result[0].name == 'Project Root'
    assert result[1].name == 'Tests'


def test_generator_sort_multi_storage_dev_cl0_config_no_filter_returns_4(
    multi_storage: ChangelistDataStorage,
    sort_config_developer_cl_0
):
    test_input = expand_changelists(multi_storage.get_changelists())
    result = list(generator_sort(test_input, sort_config_developer_cl_0, False))
    assert len(result) == 4
    assert result[0].name == 'Main'
    assert result[1].name == 'Test'
    assert result[2].name == 'Project Root'
    assert result[3].name == 'Tests'