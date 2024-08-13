""" Testing Module Sort Methods.
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting.module_sort import capitalize_words, sort_file_by_module, is_sorted_by_module
from test import data_provider
from test.data_provider import get_app_gradle_build_change_data


def test_sort_file_by_module_empty_map_empty_file_returns_false():
    cl_map = ChangelistMap()
    empty_file = ChangeData()
    assert not sort_file_by_module(cl_map, empty_file)


def test_sort_file_by_module_empty_map_module_src_file_returns_true():
    cl_map = ChangelistMap()
    src_file = ChangeData(
        after_path=data_provider.MODULE_SRC_PATH,
        after_dir=False,
    )
    assert sort_file_by_module(cl_map, src_file)
    # Check CL Map for new Changelist
    new_cl = cl_map.search('module')
    assert new_cl is not None
    assert new_cl.name == 'Module'


def test_sort_file_by_module_app_gradle_file_returns_true_inserts_build_updates():
    cl_map = ChangelistMap()
    test_file = data_provider.get_app_gradle_build_change_data()
    assert sort_file_by_module(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_file_by_module_gradle_properties_returns_true_inserts_build_updates():
    cl_map = ChangelistMap()
    test_file = data_provider.get_app_gradle_build_change_data()
    assert sort_file_by_module(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Build Updates'


def test_sort_file_by_module_github_workflows_returns_true_inserts_github():
    cl_map = ChangelistMap()
    test_file = data_provider.get_github_workflows_change_data()
    assert sort_file_by_module(cl_map, test_file)
    # Check CL Map for new Changelist
    result = cl_map.get_lists()
    assert len(result) == 1
    new_cl = result[0]
    assert len(new_cl.changes) == 1
    assert new_cl.name == 'Github'


def test_sort_file_by_module_empty_file_returns_false():
    cl_map = ChangelistMap()
    empty_file = ChangeData()
    assert not sort_file_by_module(cl_map, empty_file)


def test_is_sorted_by_module_module_cl():
    cl = data_provider.get_module_changelist()
    print(cl.get_simple_name())
    for file in cl.changes:
        assert is_sorted_by_module(cl.get_simple_name(), file)


def test_is_sorted_by_module_app_cl_app_gradle_returns_false():
    cl = data_provider.get_app_changelist()
    assert not is_sorted_by_module(
        cl.get_simple_name(), get_app_gradle_build_change_data()
    )


def test_is_sorted_by_module_app_cl_strings_res_returns_true():
    cl = data_provider.get_app_changelist()
    assert is_sorted_by_module(
        cl.get_simple_name(), data_provider.get_change_data('/app/src/main/res/values/strings.xml')
    )


def test_is_sorted_by_module_app_cl_src_file_returns_true():
    cl = data_provider.get_app_changelist()
    assert is_sorted_by_module(
        cl.get_simple_name(), data_provider.get_change_data('/app/src/main/java/app/Main.java')
    )


def test_is_sorted_by_module_build_updates_cl_returns_true():
    cl = data_provider.get_build_updates_changelist()
    for file in cl.changes:
        assert is_sorted_by_module(cl.get_simple_name(), file)


def test_is_sorted_by_module_build_updates_cl_gradle_properties_returns_true():
    cl = data_provider.get_build_updates_changelist()
    assert is_sorted_by_module(
        cl.get_simple_name(), data_provider.get_gradle_properties_change_data()
    )


def test_is_sorted_by_module_github_cl():
    cl = data_provider.get_github_changelist()
    assert is_sorted_by_module(
        cl.get_simple_name(), data_provider.get_change_data('/.github/workflow/test.yml')
    )


def test_is_sorted_by_module_github_cl():
    cl = data_provider.get_github_changelist()
    assert is_sorted_by_module(
        cl.get_simple_name(), data_provider.get_change_data('/.github/dependabot.yml')
    )


def test_captialize_word_app():
    assert capitalize_words('app') == 'App'


def test_captialize_word_gradle():
    assert capitalize_words('gradle') == 'Gradle'


def test_captialize_word_build_updates():
    assert capitalize_words('build updates') == 'Build Updates'


def test_captialize_word_root_project():
    assert capitalize_words('root project') == 'Root Project'
