""" Testing Developer Sort.
    This test module is for testing your developer file patterns and changelists.
    You should test the following two methods:
    - sort_file_by_developer
    - is_sorted_by_developer
    If you need to know which module type a file is, use helper method get_file_patterns
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.sorting import developer_sort
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.workspace.developer_changelist import DeveloperChangelist
from test import data_provider

from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import file_sort
from changelist_sort.sorting.developer_sort import sort_file_by_developer, is_sorted_by_developer


def get_file_patterns(file: ChangeData) -> tuple[DeveloperChangelist]:
    """
    Obtain the Developer Changelist Patterns that will be matched against this File Change.
    """
    module_type = file_sort.get_module_type(file)
    return developer_sort._filter_patterns_by_module(module_type)


def test_sort_file_by_developer_github_cl_exists_returns_true():
    cl_map = ChangelistMap()
    github_cl = data_provider.get_github_changelist()
    assert cl_map.insert(github_cl)
    test_file = data_provider.get_github_dependabot_change_data()
    assert sort_file_by_developer(cl_map, test_file)
    # Expect Same Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert new_cl.id == github_cl.id
    assert new_cl.name == github_cl.name
    assert new_cl.list_key == github_cl.list_key


def test_sort_file_by_developer_module_cl_creation_src_returns_true():
    cl_map = ChangelistMap()
    test_file = data_provider.get_module_src_change_data()
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(test_file) == ModuleType.MODULE
    patterns_to_match = get_file_patterns(test_file)
    # The Number of Patterns with the given ModuleType
    assert len(patterns_to_match) == 9
    #
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
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(test_file) == ModuleType.MODULE
    #
    assert is_sorted_by_developer(list_key, test_file)


def test_is_sorted_by_developer_module_cl_creation_full_key():
    list_key = ListKey('modulesourcefiles', 'Module Source Files')
    test_file = data_provider.get_module_src_change_data()
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(test_file) == ModuleType.MODULE
    #
    assert is_sorted_by_developer(list_key, test_file)
