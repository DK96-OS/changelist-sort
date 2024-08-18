""" Testing Developer Sort.
"""
from test import data_provider

from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import file_sort
from changelist_sort.sorting.developer_sort import sort_file_by_developer, is_sorted_by_developer


def test_sort_file_by_developer_github_cl_exists_returns_true():
    cl_map = ChangelistMap()
    github_cl = data_provider.get_github_changelist()
    cl_map.insert(github_cl)
    test_file = data_provider.get_github_dependabot_change_data()
    assert sort_file_by_developer(cl_map, test_file)
    # Expect New Changelist
    result = cl_map.get_lists()
    new_cl = result[0]
    assert new_cl.id == github_cl.id
    assert new_cl.name == github_cl.name
    assert new_cl.list_key == github_cl.list_key


def test_sort_file_by_developer_module_cl_creation_src_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_module_src_change_data()
    assert sort_file_by_developer(cl_map, test_file)
    # Expect New Changelist
    result = cl_map.get_lists()
    new_cl = result[0]
    # The CL Key is the Module Name
    assert new_cl.list_key.key == file_sort.get_module_name(test_file)
    # Search for CL
    assert cl_map.search(new_cl.list_key.key) is not None


def test_is_sorted_by_developer_module_cl_creation_simple_key():
    list_key = ListKey('module', 'Module Source Files')
    test_file = data_provider.get_module_src_change_data()
    #
    assert is_sorted_by_developer(list_key, test_file)


def test_is_sorted_by_developer_module_cl_creation_full_key():
    list_key = ListKey('modulesourcefiles', 'Module Source Files')
    test_file = data_provider.get_module_src_change_data()
    #
    assert is_sorted_by_developer(list_key, test_file)
