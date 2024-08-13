""" Testing Sorting Package Init Methods.
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.sorting import sort
from changelist_sort.sorting.sort_mode import SortMode
from test import data_provider


def test_sort_empty_raise_exit():
    test_input = []
    result = sort(test_input, SortMode.MODULE)
    assert result == test_input


def test_sort_no_changes_returns_same():
    test_input = [
        ChangelistData(
            id='1234',
            name='Gradle',
            changes=[],
        )
    ]
    result = sort(test_input, SortMode.MODULE)
    assert result == test_input


def test_sort_gradle_cl_gradle_file_returns_unchanged():
    test_input = [
        ChangelistData(
            id='1234',
            name='Gradle',
            changes=[
                ChangeData(
                    after_path=data_provider.APP_GRADLE_PATH,
                    after_dir=False,
                ),
            ],
        )
    ]
    result = sort(test_input, SortMode.MODULE)
    assert result == test_input
    

def test_sort_gradle_cl_gradle_files_returns_unchanged():
    test_input = [
        ChangelistData(
            id='1234',
            name='Build Updates',
            changes=[
                ChangeData(
                    after_path=data_provider.APP_GRADLE_PATH,
                    after_dir=False,
                ),
                ChangeData(
                    after_path=data_provider.ROOT_GRADLE_PATH,
                    after_dir=False,
                ),
                ChangeData(
                    after_path=data_provider.GRADLE_PROPERTIES_PATH,
                    after_dir=False,
                ),
            ],
        )
    ]
    result = sort(test_input, SortMode.MODULE)
    assert result == test_input
    

def test_sort_app_cl_gradle_file_returns_new_gradle_cl():
    test_input = [
        ChangelistData(
            id='1234',
            name='App',
            changes=[
                ChangeData(
                    after_path=data_provider.APP_GRADLE_PATH,
                    after_dir=False,
                ),
            ],
        )
    ]
    result = sort(test_input, SortMode.MODULE)
    assert result != test_input
    assert len(result) == 2
    assert result[0].name == 'App'
    assert result[1].name == 'Build Updates'
    # Check Contents of Changes List
    assert len(result[0].changes) == 0
    assert len(result[1].changes) == 1
    assert result[1].changes[0].after_path == data_provider.APP_GRADLE_PATH

