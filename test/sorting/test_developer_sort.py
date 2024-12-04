""" Testing Developer Sort.
    This test module is for testing your developer file patterns and changelists.
    You should test the following two methods:
    - sort_file_by_developer
    - is_sorted_by_developer
    If you need to know which module type a file is, use helper method get_file_patterns
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import developer_sort
from changelist_sort.sorting import file_sort
from changelist_sort.sorting.developer_sort import sort_file_by_developer, is_sorted_by_developer
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_changelist import SortingChangelist

from test.conftest import get_change_data


def get_file_patterns(file: ChangeData) ->  list[SortingChangelist]:
    """ Obtain the Developer Changelist Patterns that will be matched against this File Change.
    """
    return developer_sort.filter_patterns_by_module(file_sort.get_module_type(file))


def test_filter_patterns_by_module_root_returns_tuple():
    result = developer_sort.filter_patterns_by_module(ModuleType.ROOT)
    assert len(result) == 5


def test_filter_patterns_by_module_gradle_returns_tuple():
    result = developer_sort.filter_patterns_by_module(ModuleType.GRADLE)
    assert len(result) == 3


def test_filter_patterns_by_module_module_returns_tuple():
    result = developer_sort.filter_patterns_by_module(ModuleType.MODULE)
    assert len(result) == 9


def test_filter_patterns_by_module_hidden_returns_tuple():
    result = developer_sort.filter_patterns_by_module(ModuleType.HIDDEN)
    assert len(result) == 1


def test_sort_file_by_developer_github_cl_exists_returns_true(github_changelist, dependabot_change_data):
    cl_map = ChangelistMap()
    assert cl_map.insert(github_changelist)
    assert sort_file_by_developer(cl_map, dependabot_change_data)
    # Expect Same Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert new_cl.id == github_changelist.id
    assert new_cl.name == github_changelist.name
    assert new_cl.list_key == github_changelist.list_key


def test_sort_file_by_developer_module_cl_creation_src_returns_true(module_src_change_data):
    cl_map = ChangelistMap()
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(module_src_change_data) == ModuleType.MODULE
    patterns_to_match = get_file_patterns(module_src_change_data)
    # The Number of Patterns with the given ModuleType
    assert len(patterns_to_match) == 9
    #
    assert sort_file_by_developer(cl_map, module_src_change_data)
    # Expect New Changelist
    result = cl_map.get_lists()
    new_cl = result[0]
    # The CL Key is the Module Name
    assert new_cl.list_key.key == file_sort.get_module_name(module_src_change_data)
    # Search for CL
    assert cl_map.search(new_cl.list_key.key) is not None


def test_sort_file_by_developer_gradle_module_app_build_file_returns_true(app_gradle_build_change_data):
    cl_map = ChangelistMap()
    assert file_sort.get_module_type(app_gradle_build_change_data) == ModuleType.GRADLE
    assert sort_file_by_developer(cl_map, app_gradle_build_change_data)
    # Expect New Changelist
    result = cl_map.get_lists()
    new_cl = result[0]
    # The CL Key is the Module Name
    assert new_cl.list_key == developer_sort._BUILD_UPDATES_KEY
    # Search for CL
    assert cl_map.search(new_cl.list_key.key) is not None


def test_sort_file_by_developer_existing_gradle_module_app_build_file_returns_true(app_gradle_build_change_data):
    cl_map = ChangelistMap()
    cl_map.create_changelist(developer_sort._BUILD_UPDATES_KEY)
    assert file_sort.get_module_type(app_gradle_build_change_data) == ModuleType.GRADLE
    assert sort_file_by_developer(cl_map, app_gradle_build_change_data)
    # Expect New Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    # The CL Key is the Module Name
    assert new_cl.list_key == developer_sort._BUILD_UPDATES_KEY
    # Search for CL
    assert cl_map.search(new_cl.list_key.key) is not None


def test_sort_file_by_developer_github_workflow_github_cl_returns_true(
    github_workflows_changelist,
    github_workflows_change_data,
    sort_config_github_workflows_yml
):
    cl_map = ChangelistMap()
    assert sort_file_by_developer(cl_map, github_workflows_change_data, sort_config_github_workflows_yml)
    result = cl_map.get_lists()
    assert result[0].changes[0] == github_workflows_change_data


def test_sort_file_by_developer_gh_workflows_config_1_github_workflows_change_returns_true(
    github_workflows_changelist,
    github_workflows_change_data,
    sort_config_github_workflows_yml
):
    cl_map = ChangelistMap()
    assert sort_file_by_developer(cl_map, github_workflows_change_data, sort_config_github_workflows_yml)
    result = cl_map.get_lists()
    assert result[0].name == github_workflows_changelist.name
    assert result[0].list_key == github_workflows_changelist.list_key
    assert result[0].changes[0] == github_workflows_change_data


def test_is_sorted_by_developer_module_cl_creation_simple_key_returns_true(module_src_change_data):
    list_key = ListKey('module', 'Module Source Files')
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(module_src_change_data) == ModuleType.MODULE
    #
    assert is_sorted_by_developer(list_key, module_src_change_data, [])


def test_is_sorted_by_developer_module_cl_creation_full_key_returns_true(module_src_change_data):
    list_key = ListKey('modulesourcefiles', 'Module Source Files')
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(module_src_change_data) == ModuleType.MODULE
    #
    assert is_sorted_by_developer(list_key, module_src_change_data, [])


def test_is_sorted_by_developer_shell_script_build_file_returns_true(shell_scripts_changelist):
    list_key = ListKey('shellscripts', 'Shell Scripts')
    test_file = get_change_data('/shell_build.sh')
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(test_file) == ModuleType.ROOT
    #
    assert is_sorted_by_developer(list_key, test_file, [shell_scripts_changelist])


def test_is_sorted_by_developer_shellscripts_cl_non_shell_root_files_returns_false(shell_scripts_changelist):
    list_key = ListKey('shellscripts', 'Shell Scripts')
    test_file = get_change_data('/bat_build.bat')
    # Ensure the File is the right Module Type
    assert file_sort.get_module_type(test_file) == ModuleType.ROOT
    #
    assert not is_sorted_by_developer(list_key, test_file, [shell_scripts_changelist])
